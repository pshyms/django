from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from .models import CourseOrg, City
from .form import UserAskForm
from courses.models import Course
from operation.models import UserFavorite

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
class OrgView(View):
    def get(self, request):
        # 找到后台中添加的所有课程机构
        all_orgs = CourseOrg.objects.all()
        # 按models.py中定义的click_num反向排序，取3个
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        # 找到后台中添加的所有城市
        all_citys = City.objects.all()

        # 取出筛选城市
        city_id = request.GET.get('city', "")
        # 外键city在数据库中叫city_id,我们在机构中进一步筛选
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 类别筛选
        category = request.GET.get('ct', "")
        # 外键city在数据库中叫city_id,我们在机构中进一步筛选
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 按照学校人数或者课程数排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")

        # 移动统计结果到筛选条件之后，即可得到按条件筛选的统计结果
        org_nums = all_orgs.count()

        # 对课程机构进行分页,尝试获取从前台get请求传递来的page参数，如果是非法的参数返回第一页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 从所有机构中取出2个，每页显示2个
        p = Paginator(all_orgs, 2, request=request)
        orgs = p.page(page)

        return render(request, "org-list.html", {
            # 这里把原先的所有机构改为当前页的机构传递到前端
            "all_orgs": orgs,
            "all_citys": all_citys,
            "org_nums": org_nums,
            "city_id": city_id,
            "category": category,
            "hot_orgs": hot_orgs,
            "sort": sort,
        })


class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            # 把UserAskForm中的变量直接保存到数据库中，modelform的精髓所在
            user_ask = userask_form.save(commit=True)
            # 使用content_type指明字符串类型，浏览器才能识别
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg":"添加出错"}', content_type='application/json')


# 机构首页
class OrgHomeView(View):
    def get(self, request, org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            # operation/models->UserFavorite定义机构的类型为2
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgCourseView(View):
    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            # operation/models->UserFavorite定义机构的类型为2
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'current_page': current_page,
            'course_org': course_org,
            'has_fav': has_fav
        })


class OrgDescView(View):
    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            # operation/models->UserFavorite定义机构的类型为2
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            # operation/models->UserFavorite定义机构的类型为2
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            'course_org': course_org,
            'current_page': current_page,
            'all_teachers': all_teachers,
            'has_fav': has_fav,
        })


# 用户收藏及取消收藏
class AddFavView(View):
    def post(self, request):
        # 获得从前端传来的fav_id, fav_type
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        # 判断用户是否登陆，request有一个匿名类user，可用于判断用户是否登陆
        if not request.user.is_authenticated:
            # 如果返回fail，ajax中自动跳转等登录页面，里面的msg值要和ajax中的值相同
            return HttpResponse('{"status": "fail", "msg":"用户未登录"}', content_type='application/json')
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        # 如果记录已存在，就取消收藏
        if exist_records:
            exist_records.delete()
            return HttpResponse('{"status": "fail", "msg":收藏"}', content_type='application/json')
        # 记录不存在，就收藏
        else:
            user_fav = UserFavorite()
            # 过滤掉没取到fav_id, fav_type的默认情况
            if int(fav_type) > 0 and int(fav_id) > 0:
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.user = request.user
                user_fav.save()
                return HttpResponse('{"status": "success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status": "fail", "msg":"收藏出错"}', content_type='application/json')








