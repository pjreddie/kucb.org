from django.db import models
import datetime
import csv
from tinymce import models as tinymce_models
from django.template.defaultfilters import slugify
from kucb.news.templatetags.thumbnail import thumbnail
import random
from PIL import Image
from kucb.about.models import Bio
from kucb.news.models import StockPhoto

class Event(models.Model):
    name = models.CharField(max_length=100)

    start_date = models.DateField(help_text="Many formats supported, eg: 'October 25 2006', '2006-10-25', '10/25/2006'")
    start_time = models.TimeField(help_text="Optional, 24-hour format: hh:mm:ss or hh:mm (e.g. '12:30', '14:20:00', or '20:00')",blank=True, null=True)

    end_date = models.DateField(help_text="Optional, leave blank if it is a single day event",blank=True, null=True)
    end_time = models.TimeField(help_text="Optional",blank=True, null=True)

    location = models.CharField(help_text="Optional",max_length=100, blank=True)
    price = models.CharField(help_text="Optional",max_length=100, blank=True)
    contact = models.CharField(help_text="Optional",max_length=100, blank=True)
    age_suitability = models.CharField(help_text="Optional",max_length=100, blank=True)

    description = models.TextField(blank=True)
    slug = models.SlugField(null=True, blank=True)

    def __unicode__(self):
        return self.name


    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            l = Event.objects.filter(slug=slug)
            while len(l)>1 or (len(l)==1 and self not in l):
                slug = slug[:-4]+"".join([chr(random.randint(97,122)) for i in range(4)])
                l = Event.objects.filter(slug=slug)
            self.slug = slug

        super(Event, self).save(*args, **kwargs)

class Personal(models.Model):
    image = models.FileField(upload_to="personal")
    def __unicode__(self):
        return self.image.name

class JobPosting(models.Model):
    image = models.FileField(upload_to="jobposting")
    def __unicode__(self):
        return self.image.name

class Blot(models.Model):
    date = models.DateTimeField()
    kind = models.CharField(max_length=100, blank=True)
    details = models.TextField(blank=True)

class Scanned(models.Model):
    url = models.URLField(unique=True)
    def __unicode__(self):
        return self.url

class Content(models.Model):
    title = models.CharField(max_length=500)
    text = tinymce_models.HTMLField()
    image = models.FileField(upload_to="img", blank=True)
    def __unicode__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length = 500)
    author = models.ForeignKey(Bio, blank=True, null=True, on_delete=models.SET_NULL, related_name="posts")
    author_name = models.CharField(help_text="Optional, if author is not a user",max_length=100, blank=True, null=True)
    teaser = tinymce_models.HTMLField("Teaser intro (optional)", blank=True, default="")
    text = tinymce_models.HTMLField()
    pub_date = models.DateTimeField('Date Published')
    visible = models.BooleanField(default=True)
    stock_image = models.ForeignKey(StockPhoto, blank=True, null=True)
    image = models.FileField(upload_to="img", blank=True)
    image_caption = models.CharField(max_length=500, blank=True, default="")
    big_image = models.BooleanField(default=False)
    front_page = models.BooleanField(default=False)
    slug = models.SlugField(null=True, blank=True, unique=True, editable=False)

    @models.permalink
    def get_absolute_url(self):
        return ('kucb.community.views.post',[], {'slug':self.slug})

    def __unicode__(self):
        return self.title
    
    def image_url(self):
        if self.stock_image:
            image = self.stock_image.image
        else:
            image = self.image
        if not image:
            return ''
        elif self.big_image:
            return image.url
        else:
            return thumbnail(image)

    def full_image_url(self):
        if self.stock_image:
            image = self.stock_image.image
        else:
            image = self.image
        if not image:
            return ''
        return image.url

    def save(self, *args, **kwargs):
        if not self.author and not self.author_name:
            self.author_name = "Community News"
        if not self.slug:
            slug = slugify(self.title)
            l = Post.objects.filter(slug=slug)
            while len(l)>1 or (len(l)==1 and self not in l):
                slug = slug[:-4]+"".join([chr(random.randint(97,122)) for i in range(4)])
                l = Post.objects.filter(slug=slug)
            self.slug = slug
        super(Post, self).save(*args, **kwargs)

class Comment(models.Model):
    author = models.CharField(max_length=100)
    mail = models.EmailField(null=True)
    text = models.TextField(max_length=1000)
    date = models.DateTimeField()
    parent = models.ForeignKey(Post, related_name="comments")
    def __unicode__(self):
        return self.author + " commenting on " + self.parent.title
