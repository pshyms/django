#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.conf.urls import url
from df_goods import views
# 需要加上app_name，否则系统找不到究竟是哪个url。
app_name = 'df_goods'
urlpatterns=[
    url(r'^$',views.index),
    url(r'^list(\d+)_(\d+)_(\d+)/$', views.goodlist),
    url(r'^(\d+)/$', views.detail),
]