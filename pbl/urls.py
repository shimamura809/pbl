# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mybook.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^AIoT/', include('AIoT.urls', namespace='AIoT')),   # ←ここを追加
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static_site/(?P<path>.*)$','django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),
    )