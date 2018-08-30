from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm
from utils.email_send import send_register_email


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # get()方法只能得到一个值，防止有2个相同名字的用户,导入Q函数可以用并集(or)查询
            # django后台中密码会加密，所以不能用password=password
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            # UserProfile继承的AbstractUser中有def check_password(self, raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 当我们在urls.py中配置url后，可以自动传入request对象到对应的views.py的函数中
class LoginView(View):
    # 如果是post请求，自动调用post函数，这里重写了post函数
    def post(self, request):
        # LoginForm的参数类型规定为字典，request.POST的返回类型是QueryDict,可直接使用
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            # 验证用户名和密码是否正确，如果不正确就返回None, 正确的话就返回用户
            user = authenticate(username=user_name, password=pass_word)
            # 验证成功就登陆,并返回首页
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "index.html", {"login_form": login_form})
                else:
                    return render(request, "login.html", {"msg": "用户未激活"})
            # 表单验证成功，但是用户名或密码有误
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误"})
        # 表单验证不成功，把login_form对象返回login.html
        else:
            return render(request, "login.html", {"login_form": login_form})

    # 如果是GET类型的请求，自动调用get函数，这里重写了get函数
    def get(self, request):
        return render(request, "login.html", {})
        # render的作用是把用户的页面返回给浏览器，这里就是把login.html返回给浏览器
        # render参数中的3个变量：request, 模板名称， 空字典表示的传给前端的值，字典里的值可以直接在login.html中使用


# 注册功能的view
class RegisterView(View):
    def get(self, request):
        # 添加验证码
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        # 实例化form
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            # 如果注册用户已存在，则返回用户已存在信息，并回填注册信息
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_form, "msg": "用户已存在"})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            # 默认新建用户是不激活状态
            user_profile.is_active = False
            # pass_word是从请求中得到的明文密码，需要用make_password()转为哈希值才能保存后数据库
            user_profile.password = make_password(pass_word)
            # 保存到数据库
            user_profile.save()
            # 发送注册激活邮件
            send_register_email(user_name, "register")
            # 注册成功返回登陆页面
            return render(request, "login.html", {"register_form": register_form})
        # 验证失败返回注册页面
        else:
            return render(request, "register.html", {"register_form": register_form})


# 激活用户的view
class ActiveUserView(View):
    # active_code这个名字要和users/urls.py中path中取URL中字符串的变量名一样
    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        # 验证记录存在时
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        # 若验证记录不存在时,返回一个简单的html页面,这个页面要自己写
        else:
            return render(request, "active_fail.html")

        return render(request, "login.html")


class ForgetPwdView(View):
    # get方法直接返回页面
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        # form验证合法时取出email
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            # 发送找回密码邮件
            send_register_email(email, "forget")
            # 邮件发送完毕返回登陆页面并显示发送成功，也可以返回一个自定义网页比如send_success.html
            return render(request, "login.html", {"msg": "重置密码邮件已发送"})
        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_form})


class ResetView(View):
    # active_code这个名字要和users/urls.py中path中取URL中字符串的变量名一样
    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        # 验证记录存在时，返回重置密码页面,需要先复制到templates目录
        if all_records:
            for record in all_records:
                email = record.email
                # 把email值传回来，我们才知道是重置用户的哪个密码
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html",
                              {"email": email, "msg": "两次密码不一致"})
            user = UserProfile.objects.get(email=email)
            # pwd2是取得从前端传来的密码，为明文；而在后台中存在的密码是密文，所以需要用make_password()来加密
            user.password = make_password(pwd2)
            user.save()
            return render(request, "login.html")

        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "msg": "两次密码不一致"})





