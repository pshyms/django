# encoding = utf-8
__author__ = 'Administrator'

from .models import Course, Lesson, Video, CourseResource
import xadmin


# 课程里添加章节信息
class LessonInline(object):
    model = Lesson
    extra = 0


# 课程中添加课程资源
class CourseResourceInline(object):
    model = CourseResource
    extra = 0


# 定义courses中各模型类的管理器
class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'learn_times', 'students', 'get_zj_nums']
    search_fields = ['name', 'desc', 'detail', 'degree', 'student']
    list_filter = ['name', 'desc', 'degree', 'learn_times', 'students']
    ordering = ['-students']
    readonly_fields = ['click_nums']
    list_editable = ['degree', 'desc']
    exclude = ['fav_nums']
    # 实现课程中直接添加章节
    inlines = [LessonInline, CourseResourceInline]
    refresh_times = [3, 5]
    style_fields = {"detail": "ueditor"}

    # 字段联动
    def save_models(self):
        # 得到当前课程的实例
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            # 课程有一个外键course_org
            course_org = obj.course_org
            course_org.course_num = Course.objects.filter(course_org=course_org).count()
            course_org.save()




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

