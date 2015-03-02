# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21 03:13:22 2015

@author: Leo Furkan Isikdogan
"""

import os, re, glob, codecs, markdown, unicodedata
from dateutil.parser import parse
from jinja2 import Environment, FileSystemLoader

#parse youtube url
def youtube_code(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    youtube_regex_match = re.match(youtube_regex, url)
    if youtube_regex_match:
        return youtube_regex_match.group(6)
    return youtube_regex_match

#create url slugs from titles
def slugify(value):
    if not isinstance(value, unicode):
        value = unicode(value, 'utf8')
    value = value.replace(u'\u0131', 'i')
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return re.sub('[-\s]+', '-', value)

#strip html for the search function
def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)
    
def createBlog(text_dir, blog_dir, blog_template, createIndexPage = False, index_template = None, createSlugs = True, subdir = ""):
    #Read posts from text files
    files = glob.glob(text_dir)
    posts = []
    for file in files:
        f = codecs.open(file, "r", "utf-8")
        title = f.readline()
        date = f.readline()
        tags = f.readline().rstrip(os.linesep)
        f.readline() #skip a line
        content = f.read()
        content = markdown.markdown(content)
        
        #embed videos
        it = re.finditer("\[vid\](.*?)\[/vid\]", content)    
        for match in it:
            vidcode = youtube_code(match.group(1))
            if(vidcode != None):
                embed_code = "<div class=\"embed-responsive embed-responsive-16by9\"><iframe class=\"embed-responsive-item\" src=\"https://www.youtube.com/embed/" + vidcode + "?wmode=transparent&amp;fs=1&amp;hl=en&amp;showinfo=0&amp;iv_load_policy=3&amp;showsearch=0&amp;rel=0&amp;theme=light\"></iframe></div>"
                content = content.replace(match.group(0), embed_code)
        
        date_object = parse(date)
        formatted_date = date_object.strftime('%B %d, %Y').replace(" 0", " ")
        
        if(createSlugs):
            filename = blog_dir + slugify(title) + ".html"
        else:
            filename = blog_dir + file[0:-4] + ".html"
        
        #create a summary
        summary = content  
        #remove the first blockquote in summary
        summary = summary.replace('\n', ' ')
        summary = re.sub(r'<blockquote>(.+?)<\/blockquote>', '', summary)
        summary = striphtml(summary)[0:550]
            
        posts.append({"title": title,
                      "date": date_object,
                      "formatted_date": formatted_date,
                      "content": content,
                      "filename": filename,
                      "summary": summary,
                      "tags": tags})
    
    #template directory
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(THIS_DIR))
    
    #create HTML pages for the posts
    for post in posts:
        template = env.get_template(blog_template)
        html_file =  template.render(post = post, subdir=subdir)
        f = open(post["filename"],'w')
        f.write(html_file.encode('utf8'))
        f.close()
    
    if(createIndexPage):    
        #Sort by date
        posts = sorted(posts, key=lambda post: post["date"], reverse=True)
                
        #Parse the template
        template = env.get_template(index_template)
        html_file =  template.render(posts = posts, subdir=subdir)
        
        #Write the inex page
        f = open(blog_dir + "index.html",'w')
        f.write(html_file.encode('utf8'))
        f.close()
    