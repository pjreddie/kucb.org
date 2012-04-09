import os, sys
sys.path.append('/Users/jredmon/kucb.org')
sys.path.append('/Users/jredmon/kucb.org/kucb')
os.environ['DJANGO_SETTINGS_MODULE'] = 'kucb.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
