import json
from django.contrib.auth.models import User
users = User.objects.all()
f = open("news.json")
a = json.load(f)
for item in a:
    if item['model']=='news.article':
        if not item['fields']['author']:
            author = item['fields']['author_name'].split()
            for user in users:
                if author[0]==user.first_name:
                    item['fields']['author'] = user.pk
                    break
json.dump(a, open("news_corrected.json",'w'))
