from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django import forms
from kucb.community.models import *
from kucb.community.handle_upload import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import ModelForm, DateField, TimeField, Textarea
import random
import itertools
import datetime
import calendar
calendar.setfirstweekday(calendar.SUNDAY)

date_formats = ['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%b %d %Y', '%b %d, %Y', '%d %b %Y', '%d %b, %Y', '%B %d %Y', '%B %d, %Y','%d %B %Y', '%d %B, %Y']
time_formats = ["%H:%M","%H","%I%p","%I %p", "%I:%M%p", "%I:%M %p"]

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ('date','parent')
        widgets = {
            'text': Textarea(),
        }

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

@login_required
def upload_blotter(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                handle_uploaded_blotter(request.FILES['file'])
                return HttpResponseRedirect('/')
            except Exception as e:
                return render_to_response('500.html', {'error':e})
    else:
        form = UploadFileForm()
    return render_to_response('upload.html', {'form': form}, context_instance=RequestContext(request))

def post(request, slug):
    post = Post.objects.filter(visible=True).get(slug=slug)
    editor = request.user.is_authenticated() and request.user.is_staff
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            if request.POST['email']:
                return HttpResponseRedirect('/')
            c = form.save(commit=False)
            if not c.author:
                c.author="Anonymous"
            c.parent = post
            c.date = datetime.datetime.now()
            c.save()
            form = CommentForm()
            return HttpResponseRedirect('./#comments')
    else:
        form = CommentForm()
    comments = post.comments.all().order_by('-date')
    return render(request, 'post_full.html', {'post':post, 'form':form, 'comments':comments, "editor":editor})


def community(request):
    classifieds = list(itertools.chain(Personal.objects.all(),JobPosting.objects.all()))
    currdate = datetime.date.today()
    if len(classifieds) >= 5:
        classifieds = random.sample(classifieds, 5)
    blots = random.sample(Blot.objects.all().order_by('-date')[:40], 4)
    events = Event.objects.filter(start_date__gte = currdate).order_by('start_date')[:7]
    contents = Content.objects.all()

    post_list = Post.objects.filter(visible=True).order_by('-pub_date')
    paginator = Paginator(post_list, 3)
    page = request.GET.get('page')
    if not page:
	posts = paginator.page(1)
    else:
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
    return render_to_response('community.html',{'classifieds':classifieds,'blots':blots,'events':events, 'contents':contents,'page':posts})

def events(request, year = None, month = None ):
    date = None
    if year and month:
        date = datetime.date(int(year), int(month), 1)
    ongoing = []
    today = datetime.date.today()
    if not date:
        date = today
    first = datetime.date(date.year, date.month, 1)
    padding, num_days  = calendar.monthrange(first.year, first.month)
    padding = (padding+1)%7
    last = datetime.date(date.year, date.month, num_days)

    events = Event.objects.filter(start_date__gte = first, start_date__lte = last).order_by('start_date', 'start_time')
    day_range = [first + datetime.timedelta(days = x) for x in range(0,num_days)]
    days = [{'date':day, 'day':day.day, 'events':[]} for day in day_range]
    for event in events:
        day = event.start_date.day
        days[day-1]['events'].append(event)
    if today.year == date.year and today.month == date.month:
        days[today.day-1]['today'] = 'today'
        ongoing = Event.objects.filter(start_date__lt = today, end_date__gte =today).order_by('start_date', 'start_time')
    days = [{}]*padding + days
    end_padding = (7-len(days)%7)%7
    days = days + [{}]*end_padding
    prev_month = first - datetime.timedelta(days = 1)
    next_month = last + datetime.timedelta(days = 1)

    return render_to_response('events.html',{'date':date, 'days':days,'ongoing': ongoing, 'prev':prev_month, 'next':next_month})

def events_rss(request, num=18):
    currdate = datetime.date.today()
    events = Event.objects.filter(start_date__gte = currdate).order_by('start_date')[:num]
    return render_to_response('rss.xml',{'events':events}, mimetype='application/rss+xml')

def tot_events_rss(request):
    currdate = datetime.date.today()
    events = Event.objects.filter(start_date__gte = currdate).order_by('start_date')[:5]
    posts = Post.objects.filter(visible=True).order_by('-pub_date')[:3]
    return render_to_response('rss.xml',{'events':events, 'posts':posts}, mimetype='application/rss+xml')

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
    event = Event.objects.get(slug=slug)
    return render_to_response('single_event.html',{'event':event})

def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            new_event = form.save()
            return HttpResponseRedirect('/community/events/'+new_event.slug)
    else:
        form = EventForm()

    return render_to_response('add_event.html',{'form':form,},context_instance=RequestContext(request))
