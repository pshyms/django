from django.db import models
from datetime import datetime


# Create your models here.
# 定义城市类，可通过城市来筛选机构
class City(models.Model):
    name = models.CharField(max_length=20, verbose_name="城市")
    desc = models.CharField(max_length=200, verbose_name="城市描述")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 定义课程机构
class CourseOrg(models.Model):
    city = models.ForeignKey(City, verbose_name="所在城市", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="机构名称")
    desc = models.TextField(verbose_name="机构描述")
    # upload_to就是保存到哪个位置，没有的话会自动创建，后面的%Y,%m分别是创建年月的文件夹
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name="封面图", max_length=100)
    address = models.CharField(max_length=150, verbose_name="机构地址")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    ORG_CHOICES = (
        ("pxjg", "培训机构"),
        ("gx", "高校"),
        ("gr", "个人"),
    )
    category = models.CharField(choices=ORG_CHOICES, verbose_name="机构类别", max_length=20, default="pxjg")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    course_nums = models.IntegerField(default=0, verbose_name="课程数")

    class Meta:
        verbose_name = "课程机构"
        verbose_name_plural = verbose_name

    # 获取机构教师数
    def get_teacher_nums(self):
        return self.teacher_set.all().count()

    def __str__(self):
        return self.name


# 讲师,一个机构有很多讲师
class Teacher(models.Model):
    # 定义一个字段来指明讲师是哪个机构的
    org = models.ForeignKey(CourseOrg, verbose_name="所属机构", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="教师名称")
    work_years = models.IntegerField(default=0, verbose_name="工作年限")
    work_company = models.CharField(max_length=50, verbose_name="就职公司")
    work_position = models.CharField(max_length=50, verbose_name="公司职位")
    points = models.CharField(max_length=50, verbose_name="教学特点")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    image = models.ImageField(upload_to="teacher/%Y/%m", verbose_name="头像", max_length=100, default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "教师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name






