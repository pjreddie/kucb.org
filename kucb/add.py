import os
import sys
import datetime
from django.core.files import File
from news.models import Article, Category
from django.contrib.auth.models import User

def undohtml(html):
    return html.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"').replace('&#039;',"'").replace('&#39;',"'").replace('&#38;',"&").replace('&#038;',"&")

basedir="/Users/jredmon/Dropbox/Documents/Projects/Crawl/crawled"
dirs = [os.path.join(basedir,name) for name in os.listdir(basedir) if os.path.isdir(os.path.join(basedir,name))]
imgnames = {}
for d in dirs:
    inf = open(os.path.join(d,"article.txt")) 
    files = os.listdir(d)
    isimg = (len(files)>1)
    imgfile = ""
    if isimg:
        imgfile = [n for n in files if n != "article.txt"][0]
    article = inf.read()
    article = article.split("\n---\n")

    category = undohtml(article[0])
    title= undohtml(article[1])
    author=undohtml(article[2]).strip(">").replace("By","").strip("]").strip().split(" ")
    date = datetime.datetime.strptime(article[3], "%I:%M %p %a %B %d, %Y")
    text = article[4]

    an = ""
    a = User.objects.filter(first_name=author[0])
    if len(a):
        a = a[0]
    else:
        a = None
        an = " ".join(author)
    c = Category.objects.filter(name=category)
    if len(c):
        c = c[0]
    else:
        c = Category(name=category)
        c.save()
    
    
    for i in range(1):
        art = Article(category = c, author = a,author_name=an, title = title, pub_date=date, text = text)
        if isimg:
            if imgfile in imgnames:
                art.image = imgnames[imgfile]
            else:
                art.image.save(imgfile, File(open(os.path.join(d,imgfile))))
                imgnames[imgfile] = art.image

        print "title:",title
        art.save()
