from django.db import models
from django.contrib.auth.models import User
from tinymce import models as tinymce_models
from django.template.defaultfilters import slugify
import random
from django.core.cache import cache
from kucb.about.models import Bio

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True, editable=False)

    @models.permalink
    def get_absolute_url(self):
        return ('kucb.news.views.category',[], {'slug':self.slug})

    def __unicode__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            l = Category.objects.filter(slug=slug)
            while len(l)>1 or (len(l)==1 and self not in l):
                slug = slug[:-4]+"".join([chr(random.randint(97,122)) for i in range(4)])
                l = Category.objects.filter(slug=slug)
            self.slug = slug

        super(Category, self).save(*args, **kwargs)

class RSSHeadline(models.Model):
    title = models.CharField(max_length = 500)
    author = models.CharField(max_length = 100)
    link = models.CharField(max_length=500)
    summary = models.TextField()
    def __unicode__(self):
        return self.title

class StockPhoto(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to="img", blank=True)
    def __unicode__(self):
        return self.title

class File(models.Model):
    upload = models.FileField(upload_to="files")
    date = models.DateTimeField(auto_now_add = True)
    def __unicode__(self):
        return self.upload.url


class Article(models.Model):
    title = models.CharField(max_length = 500)
    author = models.ForeignKey(Bio, blank=True, null=True, on_delete=models.SET_NULL, related_name="articles")
    author_name = models.CharField(help_text="Optional, if author is not a user",max_length=100, blank=True, null=True)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    teaser = tinymce_models.HTMLField("Teaser intro (optional)", blank=True, default="")
    blurb = tinymce_models.HTMLField("Short intro (optional)", blank=True, default="")
    text = tinymce_models.HTMLField()
    pub_date = models.DateTimeField('Date Published')
    visible = models.BooleanField(default=True)
    stock_image = models.ForeignKey(StockPhoto, blank=True, null=True)
    image = models.FileField(upload_to="img", blank=True)
    image_caption = models.CharField(max_length=500, blank=True, default="")
    part_1 = models.FileField(upload_to="audio", blank=True)
    part_2 = models.FileField(upload_to="audio", blank=True)
    part_3 = models.FileField(upload_to="audio", blank=True)
    part_4 = models.FileField(upload_to="audio", blank=True)
    first = models.BooleanField(default=False)
    second = models.BooleanField(default=False)
    third = models.BooleanField(default=False)
    slug = models.SlugField(null=True, blank=True, unique=True, editable=False)

    @models.permalink
    def get_absolute_url(self):
        return ('kucb.news.views.article',[], {'slug':self.slug})

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.author and not self.author_name:
            self.author_name = "KUCB News"
        if not self.slug:
            slug = slugify(self.title)
            l = Article.objects.filter(slug=slug)
            while len(l)>1 or (len(l)==1 and self not in l):
                slug = slug[:-4]+"".join([chr(random.randint(97,122)) for i in range(4)])
                l = Article.objects.filter(slug=slug)
            self.slug = slug
        if self.first:
            others=Article.objects.filter(first=True)
            for a in others:
                if self != a:
                    a.first = False
                    a.save()
        if self.second:
            others=Article.objects.filter(second=True)
            for a in others:
                if self != a:
                    a.second = False
                    a.save()
        if self.third:
            others=Article.objects.filter(third=True)
            for a in others:
                if self != a:
                    a.third = False
                    a.save()
        super(Article, self).save(*args, **kwargs)

class Comment(models.Model):
    author = models.CharField(max_length=100)
    mail = models.EmailField(null=True)
    text = models.TextField(max_length=1000)
    date = models.DateTimeField()
    parent = models.ForeignKey(Article, related_name="comments")
    def __unicode__(self):
        return self.author + " commenting on " + self.parent.title
