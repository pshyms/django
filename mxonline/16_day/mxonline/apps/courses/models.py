from django.db import models
from datetime import datetime
from organization.models import CourseOrg, Teacher
from DjangoUeditor.models import UEditorField
# Create your models here.


class Course(models.Model):
    DEGREE_CHOICES = (
        ("cj", "初级"),
        ("zj", "中级"),
        ("gj", "高级")
    )
    name = models.CharField(max_length=50, verbose_name="课程名")
    desc = models.CharField(max_length=300, verbose_name="课程描述")
    # imagePath：图片的存储路径
    detail = UEditorField(verbose_name="课程详情", width=600, height=300, imagePath="courses/ueditor/",
                          filePath="courses/ueditor/", default='')
    degree = models.CharField(choices=DEGREE_CHOICES, max_length=5)
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟)")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏人数")
    # 课程的封面图片
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name="封面图", max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    course_org = models.ForeignKey(CourseOrg, verbose_name="课程机构", null=True, blank=True, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, verbose_name="课程类别", default="后端开发")
    tag = models.CharField(default="", verbose_name="课程标签", max_length=10)
    # 不能给外键指明默认值
    teacher = models.ForeignKey(Teacher, null=True, blank=True, on_delete=models.CASCADE, verbose_name="讲师")
    # 讲师提示字段
    know_first = models.CharField(max_length=200, verbose_name="课程须知", default="")
    what_to_learn = models.CharField(max_length=200, verbose_name="收获什么", default="")
    # 首页3个轮播课程的广告位
    is_banner = models.BooleanField(default=False, verbose_name="是否轮播")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    # 章节数
    def get_zj_nums(self):
        return self.lesson_set.all().count()
    get_zj_nums.short_description = "章节数"

    def get_learn_users(self):
        return self.usercourse_set.all()[:2]

    # 课程所有章节
    def get_course_lesson(self):
        return self.lesson_set.all()

    def __str__(self):
        return self.name


# 用于xadmin中注册两个模型来分类管理课程
# class BnnerCourse(Course):
#     class Meta:
#         verbose_name = "轮播课程"
#         verbose_name_plural = verbose_name
#         # 有model功能，但不生成新表
#         proxy = True


# 定义章节类,一个课程对应多个章节
class Lesson(models.Model):
    # 定义一个字段来让我们知道这个章节对应那个课程
    course = models.ForeignKey(Course, verbose_name="课程", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    # 获得章节里的所有视频
    def get_lesson_video(self):
        return self.video_set.all()

    def __str__(self):
        return "{0}--{1}".format(self.course, self.name)


# 定义每个章节的视频类,一个章节对应多个视频
class Video(models.Model):
    # 定义一个字段来存储，让我们知道这个视频对应哪个章节
    lesson = models.ForeignKey(Lesson, verbose_name="章节", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="视频名")
    url = models.CharField(max_length=200, default="", verbose_name="视频链接")
    video_time = models.IntegerField(default=0, verbose_name="视频长度(分钟)")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}--{1}".format(self.lesson, self.name)


# 课程资源，一个课程有很多资源
class CourseResource(models.Model):
    # 定义一个字段来让我们知道这个资源对应哪个课程
    course = models.ForeignKey(Course, verbose_name="课程", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="名称")
    # 资源下载地址，FileField类型在后台管理系统中会自带上传按钮，底层也是一个字符串类型，要指定最大长度
    download = models.FileField(
        upload_to="course/resource/%Y/%m",
        verbose_name="资源文件",
        max_length=100
    )
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}--{1}".format(self.course, self.name)

