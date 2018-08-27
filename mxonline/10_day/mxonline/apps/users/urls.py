__author__ = 'Administrator'
from django.urls import path
from .views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView

app_name = 'users'
urlpatterns = [
    # 这里的name指定此URL模式的名称，让我们可在其他地方用name的值引用此URL
    # LoginView.as_view()将views.py中定义的LoginView类转为view函数来使用，注意后面要有()
    path('login/', LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    # 变量active_code可取任意值，得到URL中active后面的所有字符，变量默认是字符串类型<string:active_code>
    path('active/<active_code>/', ActiveUserView.as_view(), name="user_active"),
    path('forget/', ForgetPwdView.as_view(), name="forget_pwd"),
    path('reset/<active_code>/', ResetView.as_view(), name="reset_pwd"),
    path('modify_pwd/', ModifyPwdView.as_view(), name="modify_pwd"),
]

