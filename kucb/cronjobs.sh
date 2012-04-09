#!/bin/bash

cd /usr/local/django/kucb
export DJANGO_SETTINGS_MODULE=myproject.settings 
./manage.py update_feed
