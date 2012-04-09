from django.core.management.base import BaseCommand, CommandError
from kucb.news.models import RSSHeadline
import feedparser

def ununicode(udata):
    udata = udata.replace(u'\u2013', '-')
    udata = udata.replace(u'\u2019', "'")
    udata = udata.replace(u'\u2018', "'")
    udata = udata.replace(u'\u201c', '"')
    udata = udata.replace(u'\u201d', '"')
    udata = udata.replace(u'\u2032', "'")
    return udata.encode('ascii', 'ignore')

def undohtml(html):
    return html.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"').replace('&#039;',"'").replace('&#39;',"'").replace('&#38;',"&").replace('&#038;',"&")

class Command(BaseCommand):
    args = ''
    help = 'Updates RSS Headlines'
    
    def handle(self, *args, **options):
        f = feedparser.parse('http://feeds.aprn.org/aprn-news')
        newfeed = []
        for e in f.entries[:15]:
            title = undohtml(ununicode(e.title))
            author = undohtml(ununicode(e.author))
            link = undohtml(ununicode(e.link))
            summary = undohtml(ununicode(e.summary))
            h = RSSHeadline(title=title, author = author, link=link, summary=summary)
            newfeed.append(h)
        if len(newfeed)>3:
            RSSHeadline.objects.all().delete()
            for h in newfeed:
                h.save()
            self.stdout.write('Updated headlines\n')
