from django.shortcuts import render
from .models import UserMessage
# Create your views here.


def getform(request):
    message = None
    all_message = UserMessage.objects.filter(address='西安')

    if all_message:
        # all_message是一个列表，可使用切片
        message = all_message[0]

    return render(request, 'message_form.html', {"my_message": message})



