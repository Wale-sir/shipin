from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.http import JsonResponse
from django.views.generic import View
from .models import UserProfile
from .forms import Reform, LoginForm
from django.contrib.auth import login, logout, authenticate
from my_apps.videos.models import Video
from bs4 import BeautifulSoup
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
    # def get(self,request):
    #     return render(request,'re.html',{
    #     })

    def post(self, request):
        form = Reform(request.POST)
        error = BeautifulSoup(str(form.non_field_errors()),'lxml')

        if not form.is_valid():
            return JsonResponse({'status': 'fail',
                                 'msg': '{}'.format(error.li.text)})
        # if not form.is_valid():
        #     return redirect(reverse('home'))

        # 验证通过 传入数据库
        UserProfile.objects.create_user(
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password')
        ).save()
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