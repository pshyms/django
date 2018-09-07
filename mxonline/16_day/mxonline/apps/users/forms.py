__author__ = 'Administrator'
from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile

class LoginForm(forms.Form):
    # 使用required参数指明用户名和密码不能为空
    # 这里定义的username和password必须和前端代码中input标签中的name属性值相同
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    # 这里email的名字需要和register.html中邮箱的name属性值相同
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    # 应用验证码,可自定义错误输出信息，自定义错误输出key必须和异常一样
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    # 应用验证码,可自定义错误输出信息，自定义错误输出key必须和异常一样
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})


class ModifyPwdForm(forms.Form):
    # 要输2次密码，一个为新密码，另一个为确定密码
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)


# 用于修改用户中心头像
class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


# 用于用户中心修改其他信息
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birthday', 'address', 'mobile']



