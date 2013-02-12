from kucb.about.models import Announcement, Bio, Content, Program, Schedule
from django.contrib import admin

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('program','day','start_time', 'end_time')
    ordering = ('-start_time',)

admin.site.register(Announcement)
admin.site.register(Bio)
admin.site.register(Content)
admin.site.register(Program)
admin.site.register(Schedule, ScheduleAdmin)
