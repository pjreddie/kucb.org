from django.db import models
import datetime
import csv
from tinymce import models as tinymce_models
from django.template.defaultfilters import slugify
import random
import Image

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

class Content(models.Model):
    title = models.CharField(max_length=500)
    text = tinymce_models.HTMLField()
    image = models.FileField(upload_to="img", blank=True)
    def __unicode__(self):
        return self.title

