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
        pattern = re.compile("(?P<blot>\d{1,2}/\d{1,2}/\d{1,2} .*?)(<br|</p)", flags=re.DOTALL)
        matches = pattern.finditer(r.text)
        for match in matches:
            s = match.group('blot').split(None, 3)
            if s[1] == "Tues":
                s[1] = "Tue"
            if s[1] == "Thurs":
                s[1] = "Thu"
            s[2] = '0'*(4-len(s[2])) + s[2]

            datestr = ' '.join(s[0:3])
            date = datetime.datetime.strptime(datestr, "%m/%d/%y %a %H%M")
            s[3] = s[3].replace(u'\u2013', '-')
            kind, details = s[3].split('-', 1)
            kind = kind.strip()
            details = details.strip()
            blot, created = Blot.objects.get_or_create(date=date, kind=kind)
            blot.details = details
            blot.save()
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
                self.read_blotter_url(url)
                

