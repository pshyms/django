#  coding: utf-8
from __future__ import unicode_literals
from tinymce.models import HTMLField
from django.db import models

# Create your models here.
# 商品分类
class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=20)
    #对于重要数据都做逻辑删除，不做物理删除，实现方法是定义isDelete属性，类型为BooleanField，默认值为False
    isDelete = models.BooleanField(default=False)

#在后台编辑中可以下拉菜单形式显示商品类型
    def __str__(self):
        #return self.ttitle.encode('utf-8') python2写法
        return self.ttitle


# 商品
class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=20)
    #图片位置，需要在setting中添加MEDIA_ROOT；实际部署需要在服务器部署
    gpic = models.ImageField(upload_to='df_goods')
    #总位数最多5位，小数位为2位
    gprice = models.DecimalField(max_digits=5, decimal_places=2)
    #商品不要可以逻辑删除，默认不删
    isDelete = models.BooleanField(default=False)
    #单位，可以设一个默认值500个，默认值写不写都行
    gunit = models.CharField(max_length=20, default='500g')
    #点击量，用于排序
    gclick = models.IntegerField()
    #简介
    gjianjie = models.CharField(max_length=200)
    #库存
    gkucun = models.IntegerField()
    #详细介绍，from tinymce.models import HTMLField
    gcontent = HTMLField()
    #属于哪个商品分类，这里用的django2.0,还需加上on_delete参数
    gtype = models.ForeignKey(TypeInfo, on_delete=models.CASCADE)

    def __str__(self):
        #return self.gtitle.encode('utf-8')
        return self.gtitle

