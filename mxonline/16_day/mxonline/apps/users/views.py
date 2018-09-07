from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect

from .models import UserProfile, EmailVerifyRecord, Banner
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

import json
from django.urls import reverse

# 设置邮箱可以登陆，这里的CustomBackend会被配置在setting.py中
class CustomBackend(ModelBackend):
    # 这里的authenticate是ModelBackend中的方法，我们可以自定义authenticate方法，实现可以用邮箱登陆
    # 覆盖了from django.contrib.auth import authenticate
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # get()方法只能得到一个值，防止有2个相同名字的用户,导入Q函数可以用并集(or)查询
            # django后台中密码会加密，所以不能用password=password
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            # UserProfile继承的AbstractUser中有函数check_password，它会把前端的明文密码进行加密后和后端密码对比
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 用户退出
class LogoutView(View):
    def get(self, request):
        logout(request)

        return HttpResponseRedirect(reverse("index"))


# 当我们在urls.py中配置url后，可以自动传入request对象到对应的views.py的函数中
class LoginView(View):
    # 如果是post请求，自动调用post函数，这里重写了post函数
    def post(self, request):
        # LoginForm的参数类型规定为字典，request.POST的返回类型是QueryDict,可直接使用
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")

            # 验证用户名和密码是否正确，如果不正确就返回None, 正确的话就返回用户对象，默认只能使用username完成登陆验证
            user = authenticate(username=user_name, password=pass_word)

            # 验证成功就登陆,并返回首页
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
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
            user_profile.save()

            # 用户注册时的欢迎消息
            user_message = UserMessage()
            # user字段设计时类型为IntegerField, 表示的是用户ID
            user_message.user = user_profile.id
            user_message.message = "欢迎注册我的小站"
            user_message.save()

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


# 未登陆状态下修改用户密码
class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            # 根据这个email来确定修改哪个密码
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


# 用户个人信息,需要先登陆才能访问
class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        # 这里是修改用户数据，所以需要有一个实例来指明修改哪个用户，如果不加instance的话，会增加一个新用户，不能修改
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        # 如果填写信息不全等问题，弹出错误消息
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


# 用户修改头像
class UploadImageView(LoginRequiredMixin, View):
    def post(self, request):
        # 文件上传时，是保存在request的FILES文件中的，实例化后，就把头像保存在image_form了，
        # 为modelform添加instance后，image_form就有了model的功能，可直接保存数据了
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "填写错误"}', content_type='application/json')


# 登陆状态下修改用户密码，个人中心页面
class UpdatePwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail", "msg":"密码不一致"}', content_type='application/json')
            user = request.user
            # pwd2是取得从前端传来的密码，为明文；而在后台中存在的密码是密文，所以需要用make_password()来加密
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')

        else:
            # return HttpResponse('{"status": "fail", "msg": "填写错误"}', content_type='application/json')
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


# 发送邮箱验证码，用于修改用户中心邮箱
class SendEmailCodeView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get('email', '')
        # 不能是已注册的邮箱
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email": "邮箱已存在"}', content_type='application/json')
        # 这里获得新的邮箱地址
        send_register_email(email, "update_email")
        return HttpResponse('{"status": "success"}', content_type='application/json')


# 修改用户中心邮箱
class UpdateEmailView(LoginRequiredMixin, View):
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"email": "验证码无效"}', content_type='application/json')


# 用户中心我的课程
class MyCourseView(LoginRequiredMixin, View):
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, "usercenter-mycourse.html", {"user_courses": user_courses})


# 用户中心我收藏的课程机构
class MyFavOrgView(LoginRequiredMixin, View):
    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        # fav_orgs只是存放了定义的fav_id字段，我们还需要通过fav_id得到机构对象
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            # 根据机构ID得到机构对象
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, "usercenter-fav-org.html", {"org_list": org_list})


# 用户中心我收藏的讲师
class MyFavTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, "usercenter-fav-teacher.html", {"teacher_list": teacher_list})


# 用户中心收藏的课程
class MyFavCourseView(LoginRequiredMixin, View):
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, "usercenter-fav-course.html", {"course_list": course_list})


# 用户中心我的消息
class MyMessageView(LoginRequiredMixin, View):

    def get(self, request):
        # 因为UserMessage中user字段定义为ID，那么这里的参数中也要取出当前用户的ID
        all_messages = UserMessage.objects.filter(request.user.id)

        # 用户进入个人消息后清空未读消息记录,注意需要指明当前用户
        all_unread_message = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_message:
            unread_message.has_read = True
            unread_message.save()

        # 对个人消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 从所有机构中取出2个，每页显示2个
        p = Paginator(all_messages, 2, request=request)
        messages = p.page(page)
        return render(request, "usercenter-message.html", {"messages": messages})


# 网站首页view
class IndexView(View):
    def get(self, request):
        # 取出轮播图
        all_banners = Banner.objects.all().order_by('index')[:5]
        # 正常位课程
        courses = Course.objects.filter(is_banner=False)[:6]
        # 轮播图课程取3个
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        # 课程机构
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, "index.html", {
            "all_banners": all_banners,
            "courses": courses,
            "banner_courses": banner_courses,
            "course_orgs": course_orgs,
        })




