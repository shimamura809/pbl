# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from AIoT import views
urlpatterns = patterns('',

    url(r'^datalist/$', views.datalist, name='datalist'), #datalist
    url(r'^detail/$', views.detail, name='detail'), #detail
    url(r'^pict_list/$', views.pict_list, name='pict_list'), #pict_list
    url(r'^memo_json/$', views.memo_json, name='memo_json'), #memo用json
    url(r'^threshold_json/$', views.threshold_json, name='threshold_json'), #閾値用json
    url(r'^water_json/$', views.water_json, name='water_json'), #水遣り管理用
    url(r'^getdata/$', views.getdata, name='getdata'), #取得データ一覧用
    # url(r'^datalist_json/$', views.datalist_json, name='datalist_json'), #datalist用JSON
)