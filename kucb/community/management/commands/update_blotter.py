from django.core.management.base import BaseCommand, CommandError
from kucb.community.models import Blot, Scanned
import datetime
import requests
import re


class Command(BaseCommand):
    args = ''
    help = 'Updates The Blotter'

    def read_blotter_url(self, url):
        r = requests.get(url)
        pattern = re.compile("(?P<blot>\d{1,2}/\d{1,2}/\d{1,2}.*?)(<br|</p)", flags=re.DOTALL)
        matches = pattern.finditer(r.text)
        blots = []
        for match in matches:
            s = match.group('blot').split(None, 3)
            if len(s) == 1:
                print "new format must correct"
                s = r.text[match.start():].split('</p>')[:4]
                s = [a.replace('<p>', '') for a in s]
                s = [a.replace('<div>', '') for a in s]
                s = [a.replace('\n', '') for a in s]
            orig = s
            if s[1] == "Tues":
                s[1] = "Tue"
            if s[1] == "Thurs":
                s[1] = "Thu"
            date = s[0].split("/")
            date[2] = date[2][-2:]
            s[0] = "/".join(date)
            s[2] = '0'*(4-len(s[2])) + s[2]
            try:
                time = datetime.datetime.strptime(s[2], "%H%M")
            except:
                try:
                    print "Trying colon time..."
                    if ":" in s[2]:
                        time = datetime.datetime.strptime(s[2], "%H:%M")
                    elif ";" in s[2]:
                        time = datetime.datetime.strptime(s[2], "%H;%M")
                    else:
                        print "Had to replace time:", s[2]
                        time = datetime.datetime.strptime("0000", "%H%M")
                    s[2] = time.strftime("%H%M")
                except Exception, e:
                    print "colon time:", e
                    print "Had to replace time:", s[2]
                    s[2] = "0000"
            timestamp = ' '.join(s[0:3])
            try:
                date = datetime.datetime.strptime(timestamp, "%m/%d/%y %a %H%M")
            except:
                print "Couldn't parse:", timestamp
                raise
            s[3] = s[3].replace(u'\u2013', '-')
            s[3] = s[3].replace(u'\u2014', '-')
            kind, details = s[3].split('-', 1)
            kind = kind.strip()
            details = details.strip()
            try:
                blot = Blot.objects.get(date=date, kind=kind)
            except Blot.DoesNotExist:
                blot = Blot(date=date, kind=kind)
            blot.details = details
            blots.append(blot)
        for blot in blots: blot.save()
        Scanned.objects.create(url=url)
        
    def handle(self, *args, **options):
        r = requests.get('http://www.ci.unalaska.ak.us/publicsafety/page/police-blotter')
        pattern = re.compile("/publicsafety/page/unalaska-police-blotter-\d{1,4}-\d{1,4}")
        urls = pattern.findall(r.text)
        for url in urls:
            url = 'http://www.ci.unalaska.ak.us' + url
            print url,
            try:
                Scanned.objects.get(url=url)
                print "... Found"
            except Scanned.DoesNotExist:
                print "... Being Read"
                try:
                    self.read_blotter_url(url)
                except Exception, e:
                    print "Unexpected error:", e
                

