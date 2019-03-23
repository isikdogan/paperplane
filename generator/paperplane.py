# -*- coding: utf-8 -*-
""" PaperPlane: a very simple, flat-file, static blog generator.
Created on Sat Feb 21 2015
Author: Leo Isikdogan
"""

import codecs, unicodedata
import dateutil.parser
import os, re, glob
import markdown
import jinja2

class Page:
    def __init__(self, markdown_file):
        self._read_markdown(markdown_file)
        self._parse_markdown_content()
        self._embed_videos()

    def _read_markdown(self, markdown_file):
        with codecs.open(markdown_file, "r", "utf-8") as f:
            self.title = f.readline()
            f.readline() #skip a line
            self.content = f.read()

    def _parse_markdown_content(self):
        extensions = ['markdown.extensions.extra']
        self.content = markdown.markdown(self.content, extensions=extensions)

    def get_content_text(self):
        # strips html, returns raw text
        p = re.compile(r'<.*?>')
        return p.sub('', self.content)

    def get_slugified_title(self):
        slugs = self.title
        if not isinstance(slugs, str):
            slugs = unicode(slugs, 'utf8')
        slugs = slugs.replace(u'\u0131', 'i')
        slugs = unicodedata.normalize('NFKD', slugs).encode('ascii', 'ignore').decode('ascii')
        slugs = re.sub('[^\w\s-]', '', slugs).strip().lower()
        return re.sub('[-\s]+', '-', slugs)

    @staticmethod
    def parse_youtube_url(url):
        youtube_regex = (r'(https?://)?(www\.)?'
                          '(youtube|youtu|youtube-nocookie)\.(com|be)/'
                          '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
        youtube_regex_match = re.match(youtube_regex, url)
        if youtube_regex_match:
            return youtube_regex_match.group(6)
        return youtube_regex_match

    def _embed_videos(self):
        matches = re.finditer("\[vid\](.*?)\[/vid\]", self.content)
        for match in matches:
            vidcode = self.parse_youtube_url(match.group(1))
            if(vidcode != None):
                embed_code = ('<div class="embed-responsive embed-responsive-16by9">'
                            '<iframe class="embed-responsive-item" src="https://www.youtube.com/embed/{}?'
                            'wmode=transparent&amp;fs=1&amp;hl=en&amp;showinfo=0&amp;iv_load_policy=3&amp;'
                            'showsearch=0&amp;rel=0&amp;theme=light"></iframe></div>').format(vidcode)
                self.content = self.content.replace(match.group(0), embed_code)

    def get_dictionary(self):
        return self.__dict__

class BlogPost(Page):
    def __init__(self, markdown_file):
        super().__init__(markdown_file)
        self._parse_date()
        self.filename = self.get_slugified_title() + ".html"

    def _read_markdown(self, markdown_file):
        with codecs.open(markdown_file, "r", "utf-8") as f:
            self.title = f.readline()
            self.date = f.readline()
            self.tags = f.readline().rstrip(os.linesep)
            self.description = f.readline()
            self.thumbnail = f.readline()
            f.readline() #skip a line
            self.content = f.read()
    
    def _parse_date(self):
        self.date = dateutil.parser.parse(self.date)
        self.formatted_date = self.date.strftime('%B %d, %Y').replace(" 0", " ")

class Blog:
    def __init__(self, markdown_dir):
        self.files = glob.glob(markdown_dir)
        self._create_posts()

    def _create_posts(self):
        self.posts = []
        for markdown_file in self.files:
            blog_post = BlogPost(markdown_file)
            self.posts.append(blog_post)
        # sort posts by date
        self.posts = sorted(self.posts, key=lambda post: post.date, reverse=True)

    def create_html_pages(self, blog_dir, blog_template, index_template):   
        # create blog post htmls
        for post in self.posts:
            filename = blog_dir + post.filename
            TemplateRenderer.create_html(filename, blog_template, post=post.get_dictionary(), subdir='../')
        # create index page
        filename = blog_dir + "index.html"
        TemplateRenderer.create_html(filename, index_template, posts=self.posts, subdir='../')

class TemplateRenderer:
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
    @classmethod
    def create_html(cls, filename, template, **kwargs):
        template = cls.env.get_template(template)
        html_file =  template.render(kwargs)
        with open(filename, 'wb') as f:
            f.write(html_file.encode('utf8'))

class Homepage(Page):
    def __init__(self, markdown_file):
        super().__init__(markdown_file)

    def create_html_page(self):
        TemplateRenderer.create_html('../index.html', 'homepage_template.html',
                                        post=self.get_dictionary(), subdir='')
