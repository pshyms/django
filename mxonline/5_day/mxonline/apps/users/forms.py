__author__ = 'Administrator'
from django import forms
from captcha.fields import CaptchaField

class LoginForm(forms.Form):
    # 使用required参数指明用户名和密码不能为空
    # 这里定义的username和password必须和前端代码中input标签中的name属性值相同
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    # 这里email的名字需要和register.html中邮箱的name属性值相同
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    # 应用验证码,可自定义错误输出信息
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})

