from kucb.community.models import Personal, JobPosting, Blot, Event, Content, Comment, Post, Scanned
from django.contrib import admin

class BlotAdmin(admin.ModelAdmin):
    list_display = ('kind','date', 'details')
    ordering = ('-date','kind')

class EventAdmin(admin.ModelAdmin):
    list_display = ('name','start_date','end_date')
    ordering = ('start_date','name')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author','text','date')
    ordering = ('-date',)
    readonly_fields=('author','mail','text','date','parent')

class CommentInline(admin.TabularInline):
    model=Comment
    extra=0
    readonly_fields=('author','mail','text','date','parent')

class PostAdmin(admin.ModelAdmin):
    date_hierarchy='pub_date'
    list_display = ('title','author','front_page','pub_date')
    list_editable = ('front_page',)
    ordering = ('-pub_date','title')
    fieldsets = (
        (None, {
            'fields': ('title','author','author_name','text')
        }),
        ('Image',{
            'fields': ('stock_image', 'image', 'image_caption', 'big_image')
        }),
        ('Publication Info',{
            'fields': ('pub_date','visible','front_page')
        }),
        ('Article Intros', {
            'classes': ('collapse',),
            'fields': ('teaser',)
        }),
    )
    inlines = [CommentInline]

admin.site.register(Event, EventAdmin)
admin.site.register(Personal)
admin.site.register(JobPosting)
admin.site.register(Blot, BlotAdmin)
admin.site.register(Content)
admin.site.register(Scanned)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
