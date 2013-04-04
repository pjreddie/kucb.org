import csv
import datetime
from kucb.community.models import *

def ununicode(adata):
    try:
        udata = adata.decode('utf-8')
    except:
        udata = adata.decode('latin-1')
    udata = udata.replace(u'\xd5', "'")
    udata = udata.replace(u'\xd0', '-')
    udata = udata.replace(u'\u2013', '-')
    udata = udata.replace(u'\u2019', "'")
    udata = udata.replace(u'\u2018', "'")
    udata = udata.replace(u'\u201c', '"')
    udata = udata.replace(u'\u201d', '"')
    udata = udata.replace(u'\u2032', "'")
    return udata.encode('ascii', 'ignore')
    

def handle_uploaded_blotter(f):
    destination = open('blotter.txt', 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    uploaded = open('blotter.txt','rbU')
    blots = []
    for line in csv.reader(uploaded):
        line = [ununicode(x) for x in line]
        if line and line[0]:
            line[0] = line[0].strip()
            line[1] = line[1].strip()
            if line[1] == "Tues":
                line[1] = "Tue"
            if line[1] == "Thurs":
                line[1] = "Thu"
            line[2] = line[2].strip()
            line[2] = '0'*(4-len(line[2])) + line[2]

            line[3] = line[3].strip()
            datestr = " ".join(line[0:3])
            print datestr
            date = datetime.datetime.strptime(datestr, "%m/%d/%y %a %H%M")
            dts = line[3].split("-")
            kind = dts[0].strip()
            details = "-".join(dts[1:]).strip()
            blot = Blot(date = date, kind = kind, details = details)
            blots.append(blot)
    for blot in blots:
        blot.save()


