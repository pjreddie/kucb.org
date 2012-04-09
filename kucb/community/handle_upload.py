import csv
import datetime
from kucb.community.models import *

def ununicode(adata):
    udata = adata.decode('utf-8')
    udata = udata.replace(u'\u2013', '-')
    udata = udata.replace(u'\u2019', "'")
    udata = udata.replace(u'\u2018', "'")
    udata = udata.replace(u'\u201c', '"')
    udata = udata.replace(u'\u201d', '"')
    udata = udata.replace(u'\u2032', "'")
    return udata.encode('ascii', 'ignore')
    

def handle_uploaded_blotter(f):
    destination = open('/tmp/blotter.txt', 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    uploaded = open('/tmp/blotter.txt','rb')
    for line in csv.reader(uploaded):
        try:
            line = [ununicode(x) for x in line]
            if line[0]:
                line[0] = line[0].strip()
                line[1] = line[1].strip()
                line[2] = line[2].strip()
                line[3] = line[3].strip()
                datestr = " ".join(line[0:3])
                date = datetime.datetime.strptime(datestr, "%m/%d/%y %a %H%M")
                dts = line[3].split("-")
                kind = dts[0].strip()
                details = "-".join(dts[1:]).strip()
                blot = Blot(date = date, kind = kind, details = details)
                blot.save()
        except:
            pass


