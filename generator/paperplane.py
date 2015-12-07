# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21 03:13:22 2015

@author: Leo Isikdogan
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
    
    

    #Read posts from markdown files
    files = glob.glob(text_dir)
    posts = []
    for file in files:

        md = markdown.Markdown(extensions = ['markdown.extensions.extra', 'markdown.extensions.meta'])

        f = codecs.open(file, "r", "utf-8")
        mdfile = f.read()
        content = md.convert(mdfile)
        

        #load metadata
        title = md.Meta['title'][0]

        if 'date' in md.Meta:
            date = md.Meta['date'][0]
            date_object = parse(date)
            formatted_date = date_object.strftime('%B %d, %Y').replace(" 0", " ")
        else:
            date_object = None
            formatted_date = None

        if 'description' in md.Meta:
            description = md.Meta['description'][0]
        else:
            description = content[0:500] + '...'

        if 'tags' in md.Meta:
            tags = md.Meta['tags'][0]
        else:
            tags = ""

        if 'thumbnail' in md.Meta:
            thumbnail = md.Meta['thumbnail'][0]
        else:
            thumbnail = 'https://placeholdit.imgix.net/~text?txtsize=16&txt=No+thumbnail&w=100&h=100'
        

        #embed videos
        it = re.finditer("\[vid\](.*?)\[/vid\]", content)    
        for match in it:
            vidcode = youtube_code(match.group(1))
            if(vidcode != None):
                embed_code = "<div class=\"embed-responsive embed-responsive-16by9\"><iframe class=\"embed-responsive-item\" src=\"https://www.youtube.com/embed/" + vidcode + "?wmode=transparent&amp;fs=1&amp;hl=en&amp;showinfo=0&amp;iv_load_policy=3&amp;showsearch=0&amp;rel=0&amp;theme=light\"></iframe></div>"
                content = content.replace(match.group(0), embed_code)
        
        if(createSlugs):
            filename = blog_dir + slugify(title) + ".html"
        else:
            filename = blog_dir + file[0:-3] + ".html"
        
        posts.append({"title": title,
                      "description": description,
                      "date": date_object,
                      "formatted_date": formatted_date,
                      "content": content,
                      "filename": filename,
                      "tags": tags,
                      "thumbnail": thumbnail})
    
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
        
        #Write the index page
        f = open(blog_dir + "index.html",'w')
        f.write(html_file.encode('utf8'))
        f.close()
    