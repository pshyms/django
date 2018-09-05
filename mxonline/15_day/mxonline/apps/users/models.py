# coding = utf-8
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name="昵称", default='')
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    gender = models.CharField(choices=(
        ("male", "男"), ("female", "女")
    ), default="female", max_length=10)
    address = models.CharField(max_length=100, default="")
    mobile = models.CharField(max_length=12, null=True, blank=True)
    image = models.ImageField(upload_to="image/%Y/%m", default="image/default.png", max_length=100)

    # Meta：后台栏目名
    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    # 获取用户未读消息的数量
    def unread_nums(self):
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id, has_read=False).count()


class EmailVerifyRecord(models.Model):
    SEND_CHOICES = (
        ("register", "注册"),
        ("forget", "找回密码"),
        ("update_email", "修改邮箱"),
    )
    # 下面两行没写null = True, blank = True 表示不可为空
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    send_type = models.CharField(choices=SEND_CHOICES, max_length=20)
    # 注意下面now不能加(),否则会显示编译时间，而不是实例化时间
    send_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name="标题")
    # 添加轮播图图片
    image = models.ImageField(upload_to="banner/%Y/%m", verbose_name="轮播图", max_length=100)
    # 点击轮播图跳转到的页面
    url = models.URLField(max_length=200, verbose_name="访问地址")
    # 轮播图的播放顺序
    index = models.IntegerField(default=100, verbose_name="顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name






