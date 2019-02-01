"""ssl_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from login import views as x
urlpatterns = [
    url(r'^signup/',include('signup.urls')),
    url(r'^login/$', auth_views.login, name='login'),
    #url(r'^logout/$', TemplateView.as_view(template_name='home.html'), name='log'),
    #url('', include('django.contrib.auth.urls')),
    url(r'^logout/$', x.logout_user, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'file_add/', x.create_file, name='file_add'),
   # url(r'observe/', x.create_path, name='observe'),
    url(r'file_search/', x.create_search, name='file_search'),
    url(r'file_delete/', x.create_delete, name='file_delete'),
    url(r'file_download/', x.create_download, name='file_download'),
    url(r'data/', x.data, name='file_download'),
    url(r'register/', x.register, name='register'),
    url(r'data_json/', x.download_json, name='data_json'),
    url(r'update_key/', x.user_keys, name='update_key'),
    url(r'rec/', x.create_rec, name='rec'),
    url(r'key_detail/', x.geta, name='key_detail'),
    url(r'dky_detail/', x.d_a, name='dky_detail'),
    url(r'm_b/', x.m_b, name='m_b'),
    url(r'share/', x.share_file, name='share'),
    url(r'remove/', x.share_remove, name='remove'),
    url(r'share_data1/', x.down, name='share_data1'),
    url(r'file_window/', x.openwin, name='file_window')
   # url(r'entry/', x.create_entry, name='entry'),
   # url(r'del_entry/', x.delete_entry, name='del_entry'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)
