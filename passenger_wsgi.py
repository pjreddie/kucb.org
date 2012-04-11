import os, sys
sys.path.insert(1,"/home/kucb/software/lib/python2.6/site-packages")
sys.path.append('/home/kucb/kucb.org')
sys.path.append('/home/kucb/kucb.org/kucb')
os.environ['DJANGO_SETTINGS_MODULE'] = 'kucb.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
