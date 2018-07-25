# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from df_user.models import *
from hashlib import sha1
from django.http import JsonResponse
from .islogin import islogin
from df_goods.models import GoodsInfo
from df_order.models import OrderInfo
from django.core.paginator import Paginator
from df_cart.models import *


# Create your views here.
def register(request):
    return render(request, 'df_user/register.html')


# 登入处理，register.html的form表单中数据提交到的地方
def register_handle(requst):
    response = HttpResponse()

    # 接收用户输入，下面post.get()中的参数就是register.html中input表单的name属性值
    post = requst.POST

    uname = post.get('user_name')
    upwd = post.get('pwd')
    ucpwd = post.get('cpwd')
    uemail = post.get('email')

    #判断两次密码是否一致，虽然在js中判断过一次，这里最好也做一次判断
    if upwd != ucpwd:
        return redirect('/user/register/')

    #密码加密，需要引入hashlib模块
    s1 = sha1()
    # s1.update(upwd)  python 2.7这样进行加密处理
    #python3下字符串为Unicode类型，而hash传递时需要的是utf-8类型，需转换下
    s1.update(upwd.encode("utf-8"))
    #使用hexdiget()方法可以拿到加密后的结果
    upwd3 = s1.hexdigest()

    #创建模型类对象，以便和数据库交互
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    #存到数据库
    user.save()
    #注册成功就跳转到登陆页面
    return redirect('/user/login/')

# 判断用户是否已经存在
def register_exist(requset):
    #接收get方式传过来的数据
    uname = requset.GET.get('uname')
    #django模型查询，过滤出uname,后面加上count(),如果原先有这个用户就返回1，否则返回0
    #参考https://blog.csdn.net/u014745194/article/details/74612947
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count': count})


# 登录界面
def login(request):
    uname = request.COOKIES.get('uname', '')#这个效果是从cookies中取出用户名放在显示页面
    context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 0, 'uname': uname}
    return render(request, 'df_user/login.html', context)


# 登录处理
def login_handle(request):
    # 接收请求信息
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    #这里接收的参数'jizhu'为从login.html中接收的，默认为勾选了则为1，那么就不会用后面的默认值0
    jizhu = post.get('jizhu', 0)
    # 根据用户名查询对象，这里用filter，如果查不到会返回[]
    users = UserInfo.objects.filter(uname=uname)
    # print uname
    # 判断如果未查到则用户名错，查到再判断密码是否正确，正确则转到用户中心
    if len(users) == 1:
        s1 = sha1()
        s1.update(upwd.encode("utf-8"))
        #登录带cookie值   必须 red = HttpResponseRedirect    red.set_cookie  renturn red
        if s1.hexdigest() == users[0].upwd:
            red = HttpResponseRedirect('/user/info') #转到用户中心
            count = CartInfo.objects.filter(user_id=users[0].id).count()

            #另外一种写法
            #url = request.COOKIES.get('url', '/')  这里的'/'是默认值，表示url中没设定时，转到'/'
            #red=HttpResponseRedirect(url)


            # 记住用户名，就是如果选上记住用户名勾选框，就把用户名记在cookie中
            #set_cookie()是HttpResponse中的方法，而HttpResponseRedirect继承了HttpResponse.
            if jizhu != 0:
                red.set_cookie('uname', uname)

            #如果不勾选记住用户名，就把uname值清空，max_age=-1表示立即过期，
            else:
                red.set_cookie('uname', '', max_age=-1)

            #状态保持中的session存储方式的使用，对于使用频率比较高的数据可以使用
            #存储方式包括cookie、session，会话一般指session对象
            #使用cookie，所有数据存储在客户端，注意不要存储敏感信息
            #推荐使用sesison方式，所有数据存储在服务器端，在客户端cookie中存储session_id
            #状态保持的目的是在一段时间内跟踪请求者的状态，可以实现跨页面访问当前请求者的数据
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            request.session['count'] = count
            return red #记住最后必须return

        #这里表示密码不对的处理
        else:
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname}
            return render(request, 'df_user/login.html', context)

    #这里表示没查到用户名，表明用户名错误，这里error_name设为1
    else:
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname }
        #error_name=1传到login.html中，在里面会对应的代码显示用户名错误
        return render(request, 'df_user/login.html', context)


# 登录用户中心
@islogin
def info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail

    #最近浏览，参考df_goods中的views.py
    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_id_list = goods_ids.split(',')
    #按最近浏览顺序排列
    goods_list = []
    if len(goods_ids):
        for goods_id in goods_id_list:
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))

    context = {'title': '用户中心',
               'user_email': user_email,
               'user_name': request.session['user_name'],
               'page_name': 1,
               'info': 1,
               'goods_list': goods_list}
    return render(request, 'df_user/user_center_info.html', context)


# 订单
@islogin
def order(request):
    context = {'title': '用户中心','page_name':1,'order':1}
    return render(request, 'df_user/user_center_order.html', context)


# 收货地址
@islogin
def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uphone = post.get('uphone')
        user.uyoubian = post.get('uyoubian')
        user.save()
    context = {'title': '用户中心', 'user': user, 'page_name': 1, 'site': 1}
    return render(request, 'df_user/user_center_site.html', context)


def logout(request):
    #退出时清除session，flush()：删除当前的会话数据并删除会话的Cookie
    request.session.flush()
    return redirect('/')


@islogin
def user_center_order(request, pageid):
    """
    此页面用户展示用户提交的订单，由购物车页面下单后转调过来，也可以从个人信息页面查看
    根据用户订单是否支付、下单顺序进行排序
    """

    uid = request.session.get('user_id')
    # 订单信息，根据是否支付、下单顺序进行排序
    orderinfos = OrderInfo.objects.filter(
        user_id=uid).order_by('zhifu', '-oid')

    # 分页
    #获取orderinfos list  以两个为一页的 list
    paginator = Paginator(orderinfos, 2)
    # 获取 上面集合的第 pageid 个 值
    orderlist = paginator.page(int(pageid))
    #获取一共多少 页
    plist = paginator.page_range
    #3页分页显示
    qian1 = 0
    hou = 0
    hou2 = 0
    qian2 = 0
    # dd = dangqian ye
    dd = int(pageid)
    lenn = len(plist)
    if dd>1:
        qian1 = dd-1
    if dd>=3:
        qian2 = dd-2
    if dd<lenn:
        hou = dd+1
    if dd+2<=lenn:
        hou2 = dd+2



    # 构造上下文
    context = {'page_name': 1,
               'title': '全部订单',
               'pageid': int(pageid),
               'order': 1,
               'orderlist': orderlist,
               'plist': plist,
               'pre': qian1,
               'next': hou,
               'pree': qian2,
               'lenn': lenn,
               'nextt': hou2}

    return render(request, 'df_user/user_center_order.html', context)