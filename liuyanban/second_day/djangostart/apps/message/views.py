from django.shortcuts import render
from .models import UserMessage
# Create your views here.


def getform(request):

    # 只处理post请求
    if request.method == "POST":
        # get()就是字典中普通的取值方法，取不到的话设定默认值为空
        name = request.POST.get('name', '')
        message = request.POST.get('message', '')
        address = request.POST.get('address', '')
        email = request.POST.get('email', '')

        # 实例化对象
        user_message = UserMessage()

        # 将html的值传入实例化对象
        user_message.name = name
        user_message.message = message
        user_message.address = address
        user_message.email = email
        user_message.object_id = "1452"  # 可任意写

        # 用save()保存数据
        user_message.save()

    # 数据库查询操作
    all_message = UserMessage.objects.all()
    for message in all_message:
        print(message.name)

    # 数据库删除操作，需要网页提交才能生效
    filter_message = UserMessage.objects.filter(name='hong3')
    # filter_message.delete()，只有一条数据执行这个就好
    for message1 in filter_message:
        message1.delete()

    return render(request, 'message_form.html')

