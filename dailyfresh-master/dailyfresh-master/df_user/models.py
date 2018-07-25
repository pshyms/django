# -*- coding: utf-8 -*-
# Create your models here.
from __future__ import unicode_literals
from django.db import models
class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40)
    uemail = models.CharField(max_length=30)

    #由于下面的属性没有添加到view函数中与数据库进行交互，而数据库中这几个属性值不允许为空，因此需要加上默认为空
    #收货人的名字
    ushou = models.CharField(max_length=20,default='')
    #收货地址
    uaddress = models.CharField(max_length=100,default='')
    uyoubian = models.CharField(max_length=6,default='')
    uphone = models.CharField(max_length=11,default='')

    #default和blank的更改是python层面的约束 不需要迁移，因为他们不影响数据库；
    #但是如果把default=''改为Null=True,表允许为空，虽然效果一样，但需要迁移数据库


