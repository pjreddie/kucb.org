from django.db import models
from tinymce import models as tinymce_models
from django.contrib.auth.models import User

class Content(models.Model):
    title = models.CharField(max_length=500)
    text = tinymce_models.HTMLField()
    image = models.FileField(upload_to="img", blank=True)
    def __unicode__(self):
        return self.title

class Bio(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="bio")
    name = models.CharField(max_length=100, help_text="Optional, use if not a user", blank=True, null=True)
    job_title = models.CharField(max_length=100)
    image = models.FileField(upload_to="img", blank=True)
    text = tinymce_models.HTMLField()
    def __unicode__(self):
        if self.user:
            return self.user.first_name + " " + self.user.last_name
        else:
            return self.name

    def save(self, *args, **kwargs):
        if self.user and not self.name:
            self.name = self.user.first_name + " " + self.user.last_name
        super(Bio, self).save(*args, **kwargs)

class Announcement(models.Model):
    title = models.CharField(max_length = 500)
    text = tinymce_models.HTMLField()
    pub_date = models.DateTimeField('Date Published (optional)', blank=True, null=True)
    image = models.FileField(upload_to="img", blank=True)
    active = models.BooleanField()
    def __unicode__(self):
        return self.title

