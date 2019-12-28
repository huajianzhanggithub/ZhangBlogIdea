"""ZhangBlogIdea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps import views as sitemap_views
from django.urls import path
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from blog.apis import PostViewSet, CategoryViewSet, TagViewSet
from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap
from blog.views import (
    IndexView, CategoryView, TagView, PostDetailView, SearchView, AuthorView,
)
from comment.views import CommentView
from config.views import LinkListView
from .custom_site import custom_site

# rest-framework 添加的路由
router = DefaultRouter()
router.register(r'post', PostViewSet, basename='api-post')
router.register(r'category', CategoryViewSet, basename='api-category')
router.register(r'tag', TagViewSet, basename='api-tag')

urlpatterns = [
                  path('', IndexView.as_view(), name='index'),
                  path('category/<int:category_id>/', CategoryView.as_view(), name='category-list'),
                  path('tag/<int:tag_id>/', TagView.as_view(), name='tag-list'),
                  path('post/<int:post_id>.html', PostDetailView.as_view(), name='post-detail'),
                  path('links/', LinkListView.as_view(), name='links'),
                  path('rss/', LatestPostFeed(), name='rss'),
                  path('sitemap.xml/', sitemap_views.sitemap, {'sitemaps': {'posts': PostSitemap}}),
                  path('search/', SearchView.as_view(), name='search'),
                  path('author/<int:owner_id>/', AuthorView.as_view(), name='author'),
                  path('comment/', CommentView.as_view(), name='comment'),
                  path('super_admin/', admin.site.urls, name='super-admin'),
                  path('admin/', custom_site.urls, name='admin'),
                  path('ckeditor/', include('ckeditor_uploader.urls')),
                  path('api/', include(router.urls)),
                  path('api/docs/', include_docs_urls(title='HuanJianZhang apis')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
