from django.shortcuts import render
from django.views.generic import View
from .models import CourseOrg, City


# Create your views here.
class OrgView(View):
    def get(self, request):
        # 找到后台中添加的所有课程机构
        all_orgs = CourseOrg.objects.all()
        # 找到后台中添加的所有城市
        all_citys = City.objects.all()
        org_nums = all_orgs.count()


        return render(request, "org-list.html", {
            "all_orgs": all_orgs,
            "all_citys": all_citys,
            "org_nums": org_nums,
        })

