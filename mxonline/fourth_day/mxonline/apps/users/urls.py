__author__ = 'Administrator'
from django.urls import path
from .views import my_login

app_name = 'users'
urlpatterns = [
    # 这里的name指定此URL模式的名称，让我们可在其他地方用name的值引用此URL
    path('', my_login, name="login"),
]

