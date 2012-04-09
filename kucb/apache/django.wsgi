import os, sys
sys.path.append('/usr/local/django')
sys.path.append('/usr/local/django/kucb')
os.environ['DJANGO_SETTINGS_MODULE'] = 'kucb.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
