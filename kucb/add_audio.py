from django.core.files import File
from kucb.news.models import Article

def undohtml(html):
    return html.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"').replace('&#039;',"'").replace('&#39;',"'").replace('&#38;',"&").replace('&#038;',"&")

files = {}
inf = open("crawl/full.txt").read().split('\n')
for i in range(0,len(inf)-1,3):
    files[undohtml(inf[i]).strip()] = undohtml(inf[i+1]).split("/")[-1].strip()

articles = Article.objects.all()
for art in articles:
    art.title = art.title.strip()
    art.save()

for entry in files:
    try:
        arts = Article.objects.filter(title=entry)
        if len(arts)>1:
            for art in arts:
                print art.title, art.pub_date
        for art in arts:
            art.part_1.save(art.slug+".mp3", File(open("crawl/"+files[entry])))
    except:
        print "Couldn't find:", entry
