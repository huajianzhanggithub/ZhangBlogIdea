import xadmin
from ZhangBlogIdea.custom_site import custom_site
from django.contrib import admin

from .models import Comment


# Register your models here.
@xadmin.sites.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('target', 'nickname', 'content', 'website', 'created_time')
