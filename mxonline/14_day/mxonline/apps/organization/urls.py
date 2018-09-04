__author__ = 'Administrator'
from django.urls import path
from .views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView
from .views import OrgTeacherView, AddFavView, TeacherListView, TeacherDetailView
app_name = 'organization'

urlpatterns = [
    path('list', OrgView.as_view(), name="org_list"),
    path('add_ask/', AddUserAskView.as_view(), name="add_ask"),
    path('home/<int:org_id>/', OrgHomeView.as_view(), name="org_home"),
    path('course/<int:org_id>/', OrgCourseView.as_view(), name="org_course"),
    path('desc/<int:org_id>/', OrgDescView.as_view(), name="org_desc"),
    path('org_teacher/<int:org_id>/', OrgTeacherView.as_view(), name="org_teacher"),
    # 机构收藏
    path('add_fav/', AddFavView.as_view(), name="add_fav"),
    # 讲师列表页
    path('teacher/list/', TeacherListView.as_view(), name="teacher_list"),
    # 讲师详情页
    path('teacher/detail/<int:teacher_id>/', TeacherDetailView.as_view(), name="teacher_detail"),
]

