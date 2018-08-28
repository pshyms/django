__author__ = 'Administrator'
from django.urls import path
from .views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView

app_name = 'organization'

urlpatterns = [
    path('list', OrgView.as_view(), name="org_list"),
    path('add_ask/', AddUserAskView.as_view(), name="add_ask"),
    path('home/<int:org_id>/', OrgHomeView.as_view(), name="org_home"),
    path('course/<int:org_id>/', OrgCourseView.as_view(), name="org_course"),
    path('desc/<int:org_id>/', OrgDescView.as_view(), name="org_desc"),
    path('teacher/<int:org_id>/', OrgTeacherView.as_view(), name="org_teacher"),
    # 机构收藏
    path('add_fav/', AddFavView.as_view(), name="add_fav"),
]

