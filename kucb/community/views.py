from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from kucb.community.models import *
from django.template import RequestContext
from django import forms
from kucb.community.handle_upload import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import ModelForm
import random
import itertools

class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ('slug')

class UploadFileForm(forms.Form):
    file  = forms.FileField()

def classifieds(request):
    personals = Personal.objects.all()
    jobs = JobPosting.objects.all()
    return render_to_response('classifieds.html',{'personals':personals, 'jobs':jobs})

def upload_blotter(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_blotter(request.FILES['file'])
            return HttpResponseRedirect('/')
    else:
        form = UploadFileForm()
    return render_to_response('upload.html', {'form': form}, context_instance=RequestContext(request))

def community(request):
    classifieds = list(itertools.chain(Personal.objects.all(),JobPosting.objects.all()))
    if len(classifieds) >= 5:
        classifieds = random.sample(classifieds, 5)
    blots = random.sample(Blot.objects.all().order_by('-date')[:40], 4)
    events = Event.objects.all().order_by('start_date')[:7]
    contents = Content.objects.all()
    return render_to_response('community.html',{'classifieds':classifieds,'blots':blots,'events':events, 'contents':contents})

def events(request):
    events = Event.objects.all().order_by('start_date')
    return render_to_response('events.html',{'events':events})

def blotter(request):
    blot_list = Blot.objects.all().order_by('-date')
    paginator = Paginator(blot_list, 20)
    page = request.GET.get('page')
    if not page:
        blots = paginator.page(1)
    else:
        try:
            blots = paginator.page(page)
        except PageNotAnInteger:
            blots = paginator.page(1)
        except EmptyPage:
            blots = paginator.page(paginator.num_pages)

    return render_to_response('blotter.html',{'page':blots})

def event(request, slug):
    event = [Event.objects.get(slug=slug)]
    return render_to_response('events.html',{'events':event})

def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            new_event = form.save()
            return HttpResponseRedirect('/community/events/'+new_event.slug)
    else:
        form = EventForm()

    return render_to_response('add_event.html',{'form':form,},context_instance=RequestContext(request))
