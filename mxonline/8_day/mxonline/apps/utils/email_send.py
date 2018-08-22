__author__ = 'Administrator'
from random import Random

from users.models import EmailVerifyRecord
# 导入django自带的邮箱模块
from django.core.mail import send_mail
# 导入setting中发送邮件的配置
from mxonline.settings import EMAIL_FROM


# 生成随机字符串
def random_str(random_length=8):
    str = ''
    # 生成随机字符串的可选字符串
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0, length)]
    return str


# 发送注册邮件
def send_register_email(email, send_type='register'):
    # 发送之前先保存到数据库， 到时候查询链接是否存在
    email_record = EmailVerifyRecord()
    # 生成随机的code放入链接,这里生成16位的字符串
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    # 定义邮件内容：
    email_title = ""
    email_body = ""

    # 发送类型是register时，邮箱验证send_type有2个值，register和forget，可在users/models.py中查看
    if send_type == "register":
        email_title = "hong的注册激活链接"
        email_body = "请点击链接：http://127.0.0.1:8000/active/{0}".format(code)
        # 使用django内置函数完成邮件发送，参数：主题，邮件内容，发送方，接收列表
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        # 若发送成功
        if send_status:
            pass

    # 发送类型是forget时
    elif send_type == "forget":
        email_title = "hong的密码重置链接"
        email_body = "请点击链接：http://127.0.0.1:8000/reset/{0}".format(code)
        # 使用django内置函数完成邮件发送，参数：主题，邮件内容，发送方，接收列表
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        # 若发送成功
        if send_status:
            pass



