from news.models import Article, Category, RSSHeadline, StockPhoto, Comment
from django.db import models
from django.forms.widgets import TextInput
from django.contrib import admin


class CommentAdmin(admin.ModelAdmin):
    def article_link(self, comment):
        return '<a class="nowrap" href="/admin/news/article/%d">%s</a>' % (comment.parent.id, unicode(comment.parent))
    article_link.allow_tags=True
    list_display = ('author','text','article_link','date')
    ordering = ('-date',)
    readonly_fields=('author','mail','text','date','parent')

class CommentInline(admin.TabularInline):
    model=Comment
    extra=0
    readonly_fields=('author','mail','text','date','parent')

class ArticleAdmin(admin.ModelAdmin):
    date_hierarchy='pub_date'
    list_display = ('title','author','first','second','third', 'category','pub_date')
    list_editable = ('first','second','third')
    ordering = ('-pub_date','title')
    fieldsets = (
        (None, {
            'fields': ('title','author','author_name','category','text')
        }),
        ('Image',{
            'fields': ('stock_image', 'image', 'image_caption')
        }),
        ('Audio',{
            'fields': ('part_1','part_2','part_3','part_4',)
        }),
        ('Publication Info',{
            'fields': ('pub_date','visible','first','second','third')
        }),
        ('Article Intros', {
            'classes': ('collapse',),
            'fields': ('teaser','blurb')
        }),
    )
    inlines = [CommentInline]


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(RSSHeadline)
admin.site.register(StockPhoto)
admin.site.register(Comment, CommentAdmin)
