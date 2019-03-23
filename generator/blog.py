from paperplane import Blog, Homepage, TemplateRenderer
import xml.etree.ElementTree as ET

# Posts will be read from here
markdown_dir = "posts/*.md"

# Generated pages will be written here
blog_dir = "../blog/"

# Templates
index_template = 'blog_index_template.html'
blog_template = 'blog_post_template.html'

# Create the blog
blog = Blog(markdown_dir)
blog.create_html_pages(blog_dir, blog_template, index_template)

# Create the homepage
hp = Homepage('pages/homepage.md')
hp.create_html_page()

# Create the projects page
tree = ET.parse('pages/projects.xml')
root = tree.getroot()
projects=root.findall('project')
TemplateRenderer.create_html('../projects.html',
                             'projects_template.html',
                              projects=projects, subdir='')