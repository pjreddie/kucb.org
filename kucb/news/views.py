from django.http import HttpResponseRedirect
import datetime
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, render
from kucb.news.models import Article, Category, RSSHeadline, Comment
from kucb.about.models import Announcement
from kucb.community.models import Blot, Event
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import ModelForm, Textarea
import random
from django.core.cache import cache
from django.db.models import signals

def cache_clear(sender, **kwards):
    cache.clear()

signals.post_save.connect(cache_clear, dispatch_uid="1")

def index(request):
    currdate = datetime.datetime.now()
    rangedate = currdate - datetime.timedelta(weeks=2)
    blots = random.sample(Blot.objects.all().order_by('-date')[:40], 4)
    events = Event.objects.all().order_by('start_date')[:7]
    feed = RSSHeadline.objects.all()[:7]
    articles = []
    announcements = Announcement.objects.filter(active=True)
    editor = request.user.is_authenticated() and request.user.is_staff
    try:
        first = Article.objects.get(first=True)
        articles.append(first)
    except:
        pass
    try:
        second = Article.objects.get(second=True)
        articles.append(second)
    except:
        pass
    try:
        third = Article.objects.get(third=True)
        articles.append(third)
    except:
        pass
    if len(articles)<3:
        others = Article.objects.all().order_by('-pub_date')[:3]
        articles += [n for n in others if n not in articles]
        articles = articles[:3]
    return render_to_response('index.html', {'announcements':announcements,'articles':articles, 'blots':blots, "events":events, "feed":feed, "editor":editor})

def category(request, slug):
    editor = request.user.is_authenticated() and request.user.is_staff
    category = Category.objects.get(slug = slug)
    article_list = Article.objects.filter(category=category).order_by('-pub_date')
    categories = Category.objects.all().order_by('name')
    
    paginator = Paginator(article_list, 9)
    page = request.GET.get('page')
    if not page:
        articles = paginator.page(1)
    else:
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)
    return render_to_response('news.html', {'page':articles, 'categories':categories, 'selected':slug, "editor": editor})


def news(request):
    editor = request.user.is_authenticated() and request.user.is_staff
    article_list = Article.objects.all().order_by('-pub_date')
    categories = Category.objects.all().order_by('name')
    
    paginator = Paginator(article_list, 9)
    page = request.GET.get('page')
    if not page:
        articles = paginator.page(1)
    else:
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)
    return render_to_response('news.html', {'page':articles, 'categories':categories, "editor":editor})

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ('date','parent')
        widgets = {
            'text': Textarea(),
        }


def article(request, slug):
    article = Article.objects.get(slug=slug)
    editor = request.user.is_authenticated() and request.user.is_staff
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            if request.POST['email']:
                return HttpResponseRedirect('/')
            c = form.save(commit=False)
            if not c.author:
                c.author="Anonymous"
            c.parent = article
            c.date = datetime.datetime.now()
            c.save()
            form = CommentForm()
            return HttpResponseRedirect('./#comments')
    else:
        form = CommentForm()
    comments = article.comments.all().order_by('-date')
    return render(request, 'article.html', {'article':article, 'form':form, 'comments':comments, "editor":editor})

def post(request, slug):
    if slug == "police-blotter":
        return redirect('/community/blotter/', permanent=True)
    if slug == "classifieds":
        return redirect('/community/', permanent=True)
    slug = slug.split("-")
    article = Article.objects.all()
    for s in slug:
        if s.isalpha():
            print s
            article = article.filter(slug__icontains=s)
    article = article[0]
    return redirect('/news/article/'+article.slug, permanent=True)

def sitemap(request):
    articles = Article.objects.all().order_by('-pub_date')[:1000]
    return render_to_response('article_sitemap.xml',{'articles':articles}, mimetype='application/xml')
def rss(request):
    articles = Article.objects.all().order_by('-pub_date')[:10]
    return render_to_response('rss.xml',{'articles':articles}, mimetype='application/rss+xml')
