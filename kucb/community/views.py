from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from kucb.community.models import *
from django.template import RequestContext
from django import forms
from kucb.community.handle_upload import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import ModelForm, DateField, TimeField
import random
import itertools

date_formats = ['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%b %d %Y', '%b %d, %Y', '%d %b %Y', '%d %b, %Y', '%B %d %Y', '%B %d, %Y','%d %B %Y', '%d %B, %Y']
time_formats = ["%H:%M","%H","%I%p","%I %p", "%I:%M%p", "%I:%M %p"]


class EventForm(ModelForm):
    start_date = DateField(help_text="Many formats supported, eg: 'October 25 2006', '2006-10-25', '10/25/2006'", input_formats=date_formats)
    start_time = TimeField(help_text="Optional, supported formats (12 or 24 hour): '21','21:00', '9PM', '9pm', '9:00 pm', '9:00 PM'",required=False, input_formats=time_formats)
    end_date = DateField(help_text="Optional, leave blank if it is a single day event", required=False, input_formats=date_formats)
    end_time = TimeField(help_text="Optional", required=False, input_formats=time_formats)
    class Meta:
        model = Event
        exclude = ('slug')

class UploadFileForm(forms.Form):
    file  = forms.FileField()

def classifieds(request):
    personals = Personal.objects.all().order_by('-id')
    jobs = JobPosting.objects.all().order_by('-id')
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
    events = Event.objects.filter(end_date__isnull = True).order_by('start_date')[:7]
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
