from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext
from kucb.about.models import Announcement, Bio, Content, Program, Schedule
from django.contrib.auth.models import User

def about(request, slug=None):
    contents = Content.objects.all()
    if slug:
        selected = get_object_or_404(Content, slug=slug)
    elif contents:
        selected = contents[0]
    return render_to_response('about.html', {'contents':contents, 'selected': selected})

def people(request, slug=None):
    contents = Content.objects.all()
    bios = Bio.objects.filter(visible=True).order_by('name')   
    selected = {'slug':'people'}
    return render_to_response('about_people.html', {'bios':bios,'contents':contents, 'selected': selected})

def profile(request, slug):
    bio = get_object_or_404(Bio, slug=slug)
    articles = bio.articles.filter(visible=True).order_by('-pub_date')[:10]
    editor = request.user.is_authenticated() and request.user.is_staff
    return render(request, 'profile.html', {'bio':bio, 'articles':articles, 'editor':editor})

def program(request, slug):
    program = get_object_or_404(Program, slug=slug)
    return render(request, 'program.html', {'program':program})

def schedule(request):
    programs = Schedule.objects.all().order_by('start_time')
    days = [[] for i in range(7)]
    splits = []
    for program in programs:
        if not len(splits) or program.start_time != splits[-1]:
            splits.append(program.start_time)

        lists=[]
        if program.day == -3:
            lists = days[:]
        elif program.day == -2:
            lists = days[:5]
        elif program.day == -1:
            lists = days[5:]
        else:
            lists = days[program.day:program.day+1]

        for l in lists:
            l.append(program)
    schedule = []
    for time in splits:
        start = [time]
        for day in days:
            if len(day) and day[0].start_time == time:
                start.append(day[0])
            else:
                start.append(None)
            while len(day) and day[0].start_time <= time:
                day.pop(0)
        schedule.append(start)
    return render(request, "schedule.html", {"schedule":schedule})
