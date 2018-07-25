#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/19 15:35
# @Author  : Aries
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
from django.conf.urls import url
from df_cart import views


app_name = 'df_cart'
urlpatterns=[
    url(r'^$', views.cart),
    # 下面一行第一个(\d+)表示商品ID,第二个(\d+)表示商品数量
    url(r'^add(\d+)_(\d+)/$', views.add),
    url(r'^edit(\d+)_(\d+)/$', views.edit),
    url(r'^delete(\d+)/$', views.delete),
]