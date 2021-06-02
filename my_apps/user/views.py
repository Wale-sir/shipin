from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.http import JsonResponse
from django.views.generic import View
from .models import UserProfile, EmailPro
from .forms import Reform, LoginForm, SendEmailForm
from django.contrib.auth import login, logout, authenticate
from my_apps.videos.models import Video
from utils.send_email import send_register_email
from bs4 import BeautifulSoup
import random
# Create your views here.


class UserView(View):
    """用户界面"""
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        user = UserProfile.objects.get(username=request.user)
        return render(request, 'user.html', {
            'type': 'home',
            'user': user
        })


class ReView(View):
    """注册界面"""

    def post(self, request):
        form = Reform(request.POST)
        error = BeautifulSoup(str(form.non_field_errors()),'lxml')

        if not form.is_valid():
            return JsonResponse({'status': 'fail',
                                 'msg': '{}'.format(error.li.text)})
        # if not form.is_valid():
        #     return redirect(reverse('home'))

        # 验证通过 传入数据库
        user = UserProfile.objects.create_user(
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password')
        )
        user.save()
        login(request,user)
        return JsonResponse({
            'status': 'success',
            'msg': '注册成功'
        })


class LoginView(View):
    """登录界面"""
    def get(self,request):
        if request.user.is_authenticated:
            return redirect(reverse('home'))
        return render(request,'login.html', {
            'user': request.user.is_authenticated
        })

    def post(self, request):
        form = LoginForm(request.POST)
        error = BeautifulSoup(str(form.non_field_errors()),'lxml')
        if not form.is_valid():
            return JsonResponse({
                'status': 'fail',
                'msg': error.li.text
            })

        login(request, form.cleaned_data.get('user'))
        return JsonResponse({
            'status': 'success',
            'msg': '登录成功'
        })


class LogoutView(View):
    """退出登录"""
    def get(self, request):
        logout(request)
        return redirect(reverse('home'))


class SendEmailView(View):
    """邮箱登录模块"""

    def post(self, request):
        form = SendEmailForm(request.POST)
        error = BeautifulSoup(str(form.non_field_errors()),'lxml')
        if not form.is_valid():
            return JsonResponse({
                'status': 'fail',
                'msg': error.text
            })

        username = self.generate_random_str()        # 随机生成用户名
        while UserProfile.objects.filter(username=username):
            username = self.generate_random_str()

        email = form.cleaned_data.get('email')
        UserProfile.objects.create_user(
            username=username,
            password=form.cleaned_data.get('password'),
            email=email,
            is_active=False
        ).save()

        send_register_email(email, 'register')
        return JsonResponse({
            'status': 'success',
            'msg': '邮件发送成功,请确认'
        })

    def generate_random_str(self,randomlength=16):
        """
        生成一个指定长度的随机字符串
        """
        random_str = ''
        base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
        length = len(base_str) - 1
        for i in range(randomlength):
            random_str += base_str[random.randint(0, length)]
        return random_str


class ActiveUserView(View):
    """验证邮箱登录"""
    def get(self, request, active_code):
        all_codes = EmailPro.objects.filter(code=active_code)
        if all_codes:
            for recode in all_codes:
                email = recode.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                login(request,user=user)
            return render(request, 'code.html', {
                'status': True,
                'msg': '登录成功!'
            })
        else:
            return render(request, 'code.html', {
                'status': False,
                'msg': '验证失败!'
            })
class IndexView(View):
    """个人界面"""

    def get(self,request):
        return render(request, 'index.html'
        )
class RecordView(View):
    """记录界面"""

    def get(self, request):
        return render(request, 'record.html'
                      )

class FollowView(View):
    """关注界面"""

    def get(self, request):
        return render(request, 'follow.html'
                      )



