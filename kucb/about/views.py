from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext
from kucb.about.models import Announcement, Bio, Content
from django.contrib.auth.models import User

def about(request):
    contents = Content.objects.all()
    bios = Bio.objects.all().order_by('name')   
    return render_to_response('about.html', {'bios':bios,'contents':contents})

def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    bio = user.bio.get()
    articles = user.articles.all().order_by('-pub_date')[:10]
    return render(request, 'profile.html', {'bio':bio, 'articles':articles})
