# coding = utf-8
from django.db import models
from datetime import datetime
from users.models import UserProfile
from courses.models import Course


# 用户咨询表单
class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name="姓名")
    mobile = models.CharField(max_length=11, verbose_name="手机")
    course_name = models.CharField(max_length=50, verbose_name="课程名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户咨询"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户：{0} 手机号：{1}'.format(self.name, self.mobile)


# 用户对课程的评论，这个其实是users和Courses的多对多关系,所以额外定义一个表
class CourseComments(models.Model):
    # 会涉及两个外键：用户和课程，需要import进来
    course = models.ForeignKey(Course, verbose_name="课程", on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, verbose_name="用户", on_delete=models.CASCADE)
    comments = models.CharField(max_length=250, verbose_name="评论")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="评论时间")

    class Meta:
        verbose_name = "课程评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户：{0}对于{1}的评论'.format(self.user, self.course)


# 用户收藏,页面上分为三类：课程，讲师，机构
class UserFavorite(models.Model):

    TYPE_CHOICES = (
        (1, "课程"),
        (2, "课程机构"),
        (3, "讲师")
    )
    user = models.ForeignKey(UserProfile, verbose_name="用户", on_delete=models.CASCADE)
    # 传统的方法需要涉及4个外键：用户，课程，机构，讲师
    # course = models.ForeignKey(Course, verbose_name="课程")
    # teacher = models.ForeignKey()
    # org = models.ForeignKey()
    # 其实我们可以定义一个用户收藏id来简化操作
    fav_id = models.IntegerField(default=0, verbose_name="收藏ID")
    fav_type = models.IntegerField(choices=TYPE_CHOICES, default=1, verbose_name="收藏类型")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="收藏时间")

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户{0}收藏了{1}'.format(self.user, self.fav_type)


# 用户消息表,就是发送给用户的消息
class UserMessage(models.Model):
    # 0表示发送给所有用户，不用0就是发给单独用户的ID号
    user = models.IntegerField(default=0, verbose_name="消息接收用户")
    message = models.CharField(max_length=500, verbose_name="消息内容")
    # False表未读，True表已读
    has_read = models.BooleanField(default=False, verbose_name="是否已读")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户{0}接收了{1}'.format(self.user, self.message)


# 用户课程表,涉及两个外键：用户，课程
class UserCourse(models.Model):
    course = models.ForeignKey(Course, verbose_name="课程", on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, verbose_name="用户", on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户{0}学习了{1}'.format(self.user, self.course)

