from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from kucb.about.models import Announcement, Bio, Content

def about(request):
    contents = Content.objects.all()
    bios = Bio.objects.all().order_by('name')   
    return render_to_response('about.html', {'bios':bios,'contents':contents})
