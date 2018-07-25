# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from df_user.models import UserInfo
from df_goods.models import GoodsInfo

# Create your models here.


class CartInfo(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    goods = models.ForeignKey(GoodsInfo, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)

# 在创建多对一的关系的,需要在ForeignKey参数中加入on_delete=models.CASCADE
# 主外关系键中，级联删除，也就是当删除主表的数据时候从表中的数据也随着一起删除