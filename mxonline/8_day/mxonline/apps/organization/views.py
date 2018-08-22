from django.shortcuts import render
from django.views.generic import View
from .models import CourseOrg, City

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

