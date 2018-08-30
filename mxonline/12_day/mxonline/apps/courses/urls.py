__author__ = 'Administrator'

from django.urls import path
from courses.views import CourseListView, CourseDetailView, CourseInfoView, CommentsView, AddCommentsView, VideoPlayView

app_name = 'courses'
urlpatterns = [
    path('list/', CourseListView.as_view(), name='course_list'),
    path('detail/<int:course_id>/', CourseDetailView.as_view(), name='course_detail'),
    path('info/<int:course_id>/', CourseInfoView.as_view(), name='course_info'),
    path('comments/<int:course_id>/', CommentsView.as_view(), name='course_comments'),
    path('add_comment/', AddCommentsView.as_view(), name="add_comment"),
    # 视频URL
    path('video/<int:video_id>/', VideoPlayView.as_view(), name='video_play'),
]

