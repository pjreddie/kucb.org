import json
from django.contrib.auth.models import User
f = open("news.json")
a = json.load(f)
for item in a:
    if item['model']=='news.article':
        if item['fields']['author']:
            user = User.objects.get(pk=item['fields']['author'])
            bio = user.bio.get()
            item['fields']['author'] = bio.pk
            item['fields']['author_name'] = ''
json.dump(a, open("news_corrected.json",'w'))
