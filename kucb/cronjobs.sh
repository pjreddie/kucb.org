#!/bin/bash

cd /home/kucb/kucb.org/kucb
export PYTHONPATH=$PYTHONPATH:/home/kucb/software/lib/python2.6/site-packages
export DJANGO_SETTINGS_MODULE=kucb.settings 
./manage.py update_feed
./manage.py update_events
