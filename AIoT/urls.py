# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from AIoT import views
urlpatterns = patterns('',

    url(r'^datalist/$', views.datalist, name='datalist'), #datalist
    url(r'^detail/$', views.detail, name='detail'), #detail
    # url(r'^detail_json/$', views.detail_json, name='detail_json'), #detail用json
    # url(r'^datalist_json/$', views.datalist_json, name='datalist_json'), #datalist用JSON
)