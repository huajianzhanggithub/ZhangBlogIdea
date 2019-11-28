from ZhangBlogIdea.base_admin import BaseOwnerAdmin
from ZhangBlogIdea.custom_site import custom_site
from django.contrib import admin

from .models import Link, Sidebar


# Register your models here.
@admin.register(Link, site=custom_site)
class LinkAdmin(BaseOwnerAdmin):
    list_display = ('title', 'href', 'status', 'weight', 'created_time')
    fields = ('title', 'href', 'status', 'weight')


@admin.register(Sidebar, site=custom_site)
class SidebarAdmin(BaseOwnerAdmin):
    list_display = ('title', 'display_type', 'content', 'status', 'created_time')
    fields = ('title', 'display_type', 'content')
