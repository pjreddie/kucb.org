import os, sys, site

oldpath = sys.path

sys.path = ['']

site.addsitedir('/envs/kucb/lib/python2.7/site-packages/')
site.addsitedir('/home/kucb/env/lib/python2.6/site-packages/')

sys.path.append('/home/kucb/kucb.org/')
sys.path.append('/Users/pjreddie/kucb.org/')

sys.path = sys.path + oldpath

print sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'kucb.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
