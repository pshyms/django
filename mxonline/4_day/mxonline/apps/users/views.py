from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from .models import UserProfile


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
def my_login(request):
    # 如果是POST类型的请求
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        # 验证用户名和密码是否正确，如果不正确就返回None, 正确的话就返回用户
        user = authenticate(user_name=username, pass_word=password)
        # 验证成功就登陆,并返回首页
        if user is not None and user.is_active:
            login(request, user)
            return render(request, "index.html")
        # 验证不成功还返回登陆界面
        else:
            return render(request, "login.html", {"msg": "用户名或密码错误"})

    # 如果是GET类型的请求，就返回登陆界面
    elif request.method == "GET":
        return render(request, "login.html", {})
    # render的作用是把用户的页面返回给浏览器，这里就是把login.html返回给浏览器
    # render参数中的3个变量：request, 模板名称， 一个字典格式表示的传给前端的值，这里定义的话，字典里的值可以直接在login.html中使用


