from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course, CourseResource, Video
from operation.models import UserFavorite, CourseComments, UserCourse
from django.http import HttpResponse
from apps.utils.mixin_utils import LoginRequiredMixin
from django.db.models import Q


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]

        # 课程搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords) |
                                             Q(desc__icontains=search_keywords) | Q(detail__icontains=search_keywords))

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
            "search_keywords": search_keywords,
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
class CourseInfoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        # 参数中的id为数据库中自动生成的，course_id为URL中截取的
        course = Course.objects.get(id=course_id)
        # 查询用户是否已关联该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        # 取出这门课的用户课程表
        user_courses = UserCourse.objects.filter(course=course)
        # 使用列表推导式取出这门课用户课程表中的所有用户id，UserCourse有一个user字段，user有一个id属性
        user_ids = [user_course.user.id for user_course in user_courses]
        # 取到这些用户的所有课程，user是UserCourse中的外键，所以可直接用user_id取到user的ID，而不用实例化对象
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出上面用户课程表中所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 获取学过该课程的用户还学过的其他课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")

        all_resources = CourseResource.objects.filter(course=course)
        return render(request, "course-video.html", {
            "course": course,
            "all_resources": all_resources,
            "relate_courses": relate_courses,
        })


# 课程评论
class CommentsView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.all()
        return render(request, "course-comment.html", {
            "course": course,
            "all_resources": all_resources,
            "all_comments": all_comments,
        })


# ajax方式添加评论
class AddCommentsView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            # 未登陆时返回json提示未登陆，跳转到登陆页面是在ajax中做的
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}', content_type='application/json')
        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")

        if int(course_id) > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))

            # CourseComments中有一个外键指向Course,存入外键时要存入对象
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            # 返回格式为和前端约定的一种格式
            return HttpResponse('{"status": "success", "msg": "评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "评论失败"}', content_type='application/json')


# 视频播放view
class VideoPlayView(View):
    def get(self, request, video_id):
        video = Video.objects.get(id=video_id)
        # 找到对应的course
        course = video.lesson.course

        # 查询用户是否已关联该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        # 取出这门课的用户课程表
        user_courses = UserCourse.objects.filter(course=course)
        # 取出用户课程表中的所有用户ID
        user_ids = [user_course.user.id for user_course in user_courses]
        # 取到这些用户的所有课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出上面用户课程表中所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 获取学过该课程的用户还学过的其他课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, "course-play.html", {
            "course": course,
            "all_resources": all_resources,
            "relate_courses": relate_courses,
            "video": video,
        })
