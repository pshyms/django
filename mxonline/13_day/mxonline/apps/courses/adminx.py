# encoding = utf-8
__author__ = 'Administrator'

from .models import Course, Lesson, Video, CourseResource
import xadmin


# 定义courses中各模型类的管理器
class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'student']
    list_filter = ['name', 'desc', 'degree', 'learn_times', 'students']


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['name', 'lesson', 'add_time']
    search_fields = ['name', 'lesson']
    list_filter = ['name', 'lesson', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    # __name代表使用外键中的name字段
    list_filter = ['course__name', 'name', 'download', 'add_time']


# 将管理器与model进行关联注册
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)

