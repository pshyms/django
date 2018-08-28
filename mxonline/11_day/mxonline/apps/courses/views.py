from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course, CourseResource
from operation.models import UserFavorite

class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]

        # 课程排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")

        # 课程分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 设定每页显示3个
        p = Paginator(all_courses, 3, request=request)
        # 取到分页的课程并赋值给变量courses
        courses = p.page(page)

        return render(request, "course-list.html", {
            "all_courses": courses,
            "sort": sort,
            "hot_courses": hot_courses,
        })


# 课程详情页
class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        # 增加课程点击数
        course.click_nums += 1
        course.save()
        # 默认不收藏课程
        has_fav_course = False
        has_fav_org = False
        # 用户登陆的情况下
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        # 相关课程推荐
        tag = course.tag
        if tag:
            # 需要从1开始，否则会推荐自己
            relate_courses = Course.objects.filter(tag=tag)[1:2]
        else:
            relate_courses = []

        return render(request, "course-detail.html", {
            "course": course,
            "relate_courses": relate_courses,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org,
        })


# 课程章节信息页面
class CourseInfoView(View):
    def get(self, request, course_id):
        # 参数中的id为数据库中自动生成的，course_id为URL中截取的
        course = Course.objects.get(id=course_id)
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, "course-video.html", {
            "course": course,
            "all_resources": all_resources,
        })
