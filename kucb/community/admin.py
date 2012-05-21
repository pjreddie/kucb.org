from kucb.community.models import Personal, JobPosting, Blot, Event, Content
from django.contrib import admin

class BlotAdmin(admin.ModelAdmin):
    list_display = ('kind','date', 'details')
    ordering = ('-date','kind')

class EventAdmin(admin.ModelAdmin):
    list_display = ('name','start_date','end_date')
    ordering = ('start_date','name')

admin.site.register(Event, EventAdmin)
admin.site.register(Personal)
admin.site.register(JobPosting)
admin.site.register(Blot, BlotAdmin)
admin.site.register(Content)
