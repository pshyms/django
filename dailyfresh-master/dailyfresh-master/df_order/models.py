# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from df_user.models import UserInfo
# Create your models here.


class OrderInfo(models.Model):
    oid = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey(UserInfo,  on_delete=models.CASCADE)
    odate = models.DateTimeField(auto_now=True)
    oIsPay = models.IntegerField(default=0)
    ototal = models.DecimalField(max_digits=6, decimal_places=2)
    oaddress = models.CharField(max_length=150, default='')
    zhifu = models.IntegerField(default=0)

class OrderDetailInfo(models.Model):
    goods = models.ForeignKey('df_goods.GoodsInfo', on_delete=models.CASCADE)
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE )
    price = models.DecimalField(max_digits=5, decimal_places=2)
    count = models.Integer Field()