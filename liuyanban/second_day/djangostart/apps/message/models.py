
# coding = utf-8
from django.db import models


class UserMessage(models.Model):
    object_id = models.CharField(primary_key=True, max_length=20, default="", verbose_name="主键")
    name = models.CharField(max_length=20, blank=True, null=True, verbose_name="用户名")
    email = models.EmailField(verbose_name="邮箱")
    address = models.CharField(max_length=100, verbose_name="联系地址")
    message = models.CharField(max_length=500, verbose_name="留言信息")

    class Meta:
        verbose_name = "用户留言信息"
        verbose_name_plural = verbose_name
        ordering = ['-object_id']
        db_table = 'user_message'