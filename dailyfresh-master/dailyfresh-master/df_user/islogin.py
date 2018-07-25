#coding=utf-8
from django.http import HttpResponseRedirect

#如果登录则转到登录页面
def islogin(func):
    def login_fun(request, *args, **kwargs):
        if request.session.get('user_id'):
            return func(request, *args, **kwargs)
        else:
            #没登陆的情况
            red = HttpResponseRedirect('/user/login')
            #下面set_cookie()参数中，url是键名，request.get_full_path()的值是键值，下面一行代码的作用是记录来源页面，从哪来回哪去
            red.set_cookie('url', request.get_full_path())
            return red
    return login_fun

"""
例如：http://127.0.0.1:8080/200/?type=10
request.path：表示当前路径,为/200/
request.get_full_path()：表示完整路径，为/200/？type=10,这里的作用是记录来源页面
"""