#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/18 17:57
# @Author  : Aries
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
from django.conf.urls import url
from . import views
app_name = 'df_user'
urlpatterns=[
    url(r'^register/$', views.register),
    url(r'^register_handle/$', views.register_handle),
    url(r'^register_exist/$', views.register_exist),
    url(r'^login_handle/$', views.login_handle),
    url(r'^login/$', views.login),
    url(r'^info/$', views.info),
    #url(r'^order/', views.order),
    url(r'^site/$', views.site),
    url(r'^logout/$', views.logout),
    url(r'^user_center_order&(\d+)/$', views.user_center_order),
]
