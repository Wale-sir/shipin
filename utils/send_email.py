from random import Random
from django.core.mail import send_mail
from my_apps.user.models import EmailPro
from Jv.settings import EMAIL_FROM


def random_str(randomlength=8):
    """字符串生成"""
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars)-1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str   # 将拼接的字符串返回


def send_register_email(email, send_type='register'):  # 类型为注册
    """接收两个参数，一个邮箱，另一个是发送类型，注册或忘记密码"""
    email_recode = EmailPro()
    code = random_str(16)  # 生成16位的随机字符串
    email_recode.code = code
    email_recode.email = email
    email_recode.send_type = send_type
    email_recode.save()

    email_title = 'django 测试'
    email_body = '这是一个django测试'

    if send_type == 'register':
        email_title = '注册激活链接'
        email_body = '请点击下方的链接激活你的账号：http://127.0.0.1:8000/user/active/{0}'.format(code)
    else:
        pass  # 忘记密码--暂时不写
    send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])  # 注释 ①
    if send_status:
        pass
