# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21 03:13:22 2015

@author: Leo Furkan Isikdogan
"""

from paperplane import createBlog
import os

#Posts will be read from here
text_dir = "posts/*.txt"
frontpage_text_dir = "index.txt"

#Generated pages will be written here
blog_dir = "../blog/"
frontpage_dir = "../"

#Templates
index_template = 'blog_index_template.html'
blog_template = 'blog_post_template.html'
frontpage_template = 'frontpage_template.html'

#Create the blog
createBlog(text_dir, blog_dir, blog_template, createIndexPage = True, index_template = index_template, subdir = "../")
                                         
#Create the frontpage
createBlog(frontpage_text_dir, frontpage_dir, frontpage_template, createSlugs = False)