PaperPlane is a very simple, flat-file, static blog generator. Originally, I made it to create [my homepage](http://www.isikdogan.com/). Feel free to use it to create yours.

[Live demo (my personal homepage)](http://www.isikdogan.com/)  
Install dependencies using `pip install -r requirements.txt`  
Then run `generator/blog.py` to create a static website.  

#### Features
PaperPlane is fast. The pages are all pre-rendered therefore load fast. No server-side querying is needed to display the pages. It requires no database. The data is stored in a folder containing a flat text file for each blog entry. No scripts run on the server side. Therefore, PaperPlane generated blogs can run on any HTML hosting service (Google Cloud Storage, GitHub, Dropbox, etc.).  
It's easy to create content using PaperPlane. PaperPlane supports simple [Markdown](http://daringfireball.net/projects/markdown/) formatting. You can also easily embed videos using `[vid]link[/vid]` tags.  
It's easy to use custom themes with PaperPlane. PaperPlane uses [Jinja2](http://jinja.pocoo.org/docs/dev/) template engine, [Bootstrap 3.0](http://getbootstrap.com/) HTML/CSS framework, and [FontAwesome](http://fontawesome.io/) icon collection.

#### TODO & Missing Features
* Menu items are hard coded into the template. They should be automatically generated.
* Pagination is not supported.
* The search function searches only in the current page.
* Tags are not clickable.

#### Free and open source
The PaperPlane project is released under the terms of the [MIT license](http://en.wikipedia.org/wiki/MIT_License). You can download or fork the code on [GitHub](https://github.com/isikdogan/paperplane). I would appreciate any contributions and merge requests.
