__author__ = 'Administrator'
from django.urls import path
from .views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, SendEmailCodeView
from .views import ResetView, ModifyPwdView, UserInfoView, UploadImageView, UpdatePwdView, UpdateEmailView

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
    # 用户中心页面
    path('info/', UserInfoView.as_view(), name="info"),
    # 用户头像上传
    path('image/upload/', UploadImageView.as_view(), name="image_upload"),
    # 用户中心修改密码
    path('update/pwd/', UpdatePwdView.as_view(), name="update_pwd"),
    # 发送邮箱验证码，用于用户中心修改邮箱,注意后面的"/"一定不能少
    path('send_email_code/', SendEmailCodeView.as_view(), name="send_email_code"),
    # 修改用户中心邮箱地址
    path('update_email/', UpdateEmailView.as_view(), name="update_email"),




]

