from django.shortcuts import render, redirect, reverse, HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.views.generic import View
from .models import UserProfile, EmailPro, UserFavorite, UserMessage
from .forms import Reform, LoginForm, SendEmailForm, AddFavForm, ChangePicForm, ChangeInfoForm
from django.contrib.auth import login, logout, authenticate
from my_apps.videos.models import Video, VideoHistory, VideoStar
from utils.send_email import send_register_email, random_str
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


class UserView(View):
    """用户界面"""
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        user = request.user.is_authenticated

        all_videos = []
        all_star = []
        # 搜藏
        user_fav = UserFavorite.objects.filter(user=request.user)
        for fav in user_fav:
            if fav.fav_type == '1':
                video = Video.objects.get(id=fav.fav_id)
                all_videos.append(video)
            elif fav.fav_type == '2':
                star = VideoStar.objects.get(id=fav.fav_id)
                all_star.append(star)

        # 进入个人主页时,删除一些历史记录
        self.del_history(request.user)

        # 获取所有的观看记录
        all_video_history = VideoHistory.objects.filter(user=request.user).order_by('-modify_time')
        return render(request, 'user.html', {
            'type': 'home',
            'user_is_au': user,
            'all_videos': all_videos[:3],
            'all_star': all_star[:3],
            'all_video_history': all_video_history[:3],
            'pic_form': ChangePicForm()
        })

    def del_history(self, user):
        """
        进入个人主页时
        历史记录自动删除一部分
        """
        # 如果此用户的所有历史记录大于一定数量
        if VideoHistory.objects.filter(user=user).count() > 40:
            vs = VideoHistory.objects.filter(user=user).order_by('-modify_time')
            for i in vs[40:]:
                i.delete()


class UserFavView(View):
    """用户收藏界面"""

    def get(self,request):
        if not request.user.is_authenticated:
            return redirect(reverse('home'))
        data = {}

        data['user_is_au'] = request.user.is_authenticated

        all_videos = []
        all_star = []
        # 视频搜藏查询
        user_fav = UserFavorite.objects.filter(user=request.user)
        for fav in user_fav:
            if fav.fav_type == '1':
                video = Video.objects.get(id=fav.fav_id)
                all_videos.append(video)
            elif fav.fav_type == '2':
                star = VideoStar.objects.get(id=fav.fav_id)
                all_star.append(star)

        # 视频分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_videos, per_page=20, request=request)
        all_video = p.page(page)

        data['all_video'] = all_video

        # 所有明星分页
        try:
            page = request.GET.get('star_page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_star, per_page=20, request=request)
        all_star = p.page(page)

        data['all_star'] = all_star
        return render(request,'user_fav.html',data)


class ChangePassword(View):
    def post(self, request):
        form = ChangePasswordForm(request.POST)

        return JsonResponse({
            'status': 'fail',
            'msg': form.non_field_errors()
        })


class UserHistory(View):
    def get(self,request):
        data = {}
        data['user_is_au'] = request.user.is_authenticated

        all_video_history = VideoHistory.objects.filter(user=request.user).order_by('-modify_time')
        # 历史记录分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_video_history, per_page=20, request=request)
        all_video_history = p.page(page)

        data['all_video_history'] = all_video_history
        return render(request,'user_history.html',data)


class ChangePic(View):
    """修改用户头像"""
    def post(self,request):
        image_form = ChangePicForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return redirect(reverse('user'))
        else:
            return redirect(reverse('user'))


class ChangeInfo(View):
    def post(self,request):
        form = ChangeInfoForm(request.POST)
        if form.is_valid():
            nick_name = form.cleaned_data['nick_name']
            birthday = form.cleaned_data['birthday']
            gender = form.cleaned_data['gender']
            address = form.cleaned_data['address']
            user = request.user
            user.nick_name = nick_name
            user.birthday = birthday
            user.gender = gender
            user.address = address
            user.save()
            return redirect(reverse('user'))
        else:
            return redirect(reverse('user'))




class ReView(View):
    """注册界面"""

    def get(self,request):
        re_form = Reform()
        means = request.GET.get('means')
        if means == 'email':
            re_form = SendEmailForm()
        return render(request, 'register.html', {
            're_form': re_form,
            'means': means
        })

    def post(self, request):
        re_form = Reform(request.POST)

        if not re_form.is_valid():
            return render(request,'register.html',{
                're_form': re_form,
                'error': re_form.non_field_errors})

        # 验证通过 传入数据库
        user = UserProfile.objects.create_user(
            username=re_form.cleaned_data.get('username'),
            password=re_form.cleaned_data.get('password')
        )
        user.save()
        login(request,user)
        return redirect(reverse('home'))


class LoginView(View):
    """登录功能"""

    def get(self,request):
        if request.user.is_authenticated:
            return redirect(reverse('home'))
        form = LoginForm()
        return render(request, 'login.html', {
            'login_form': form
        })

    def post(self, request):
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request,'login.html',{
                'login_form': form,
                'error': form.non_field_errors
            })

        login(request, form.cleaned_data.get('user'))
        return redirect(reverse('home'))


class LogoutView(View):
    """退出登录"""
    def get(self, request):
        logout(request)
        return redirect(reverse('home'))


class SendEmailView(View):
    """邮箱登录模块"""

    def post(self, request):
        form = SendEmailForm(request.POST)
        if not form.is_valid():
            return render(request,'register.html',{
                're_form': form,
                'error_re_email': form.non_field_errors,
                'means': 'email'
            })

        username = random_str()       # 随机生成用户名
        while UserProfile.objects.filter(username=username):
            username = random_str()

        email = form.cleaned_data.get('email')
        UserProfile.objects.create_user(
            username=username,
            password=form.cleaned_data.get('password'),
            email=email,
            is_active=False
        ).save()

        send_register_email(email, 'register')

        # 主页信息
        data = {}
        if request.user.is_authenticated:
            user = UserProfile.objects.get(
                username=request.user
            )
            data['username'] = user.username
        data['user_is_au'] = request.user.is_authenticated
        data['login_form'] = LoginForm()
        video_list = Video.objects.all()
        data['video_list'] = video_list
        data['msg'] = 're_em_msg'
        return render(request, 'home.html', data)


class ActiveUserView(View):
    """邮箱验证登录模块"""
    def get(self, request, active_code):
        all_codes = EmailPro.objects.filter(code=active_code)
        if all_codes:
            for recode in all_codes:
                email = recode.email
                user = UserProfile.objects.get(email=email)
                # 激活用户
                user.is_active = True
                user.save()
                login(request,user=user)
                # 验证成功之后删除验证码
                recode.delete()
            return render(request, 'code.html', {
                'status': True,
                'msg': '登录成功!'
            })
        else:
            for recode in all_codes:
                # 删除数据库中的验证码
                recode.delete()
            return render(request, 'code.html', {
                'status': False,
                'msg': '验证失败!'
            })


class FavView(View):
    """收藏功能"""

    def post(self,request):
        form = AddFavForm(request.POST)
        if form.is_valid():
            user = request.user
            fav_id = form.cleaned_data['fav_id']
            fav_type = form.cleaned_data['fav_type']
            # 查看是否被收藏
            us = UserFavorite.objects.filter(
                user=user,
                fav_id=fav_id,
                fav_type=fav_type
            )
            if us:
                us.delete()
                if fav_type == '1':
                    video = Video.objects.get(id=fav_id)
                    video.hav_num -= 1
                    if video.hav_num < 0:
                        video.hav_num = 0
                    video.save()
                elif fav_type == '2':
                    user = VideoStar.objects.get(id=fav_id).user
                    user.fans -= 1
                    if user.hav_num < 0:
                        user.hav_num = 0
                    user.save()
                return JsonResponse({
                    'status': 'success',
                    'msg': '追番'
                })

            else:
                UserFavorite.objects.create(
                        user=user,
                        fav_id=fav_id,
                        fav_type=fav_type
                    ).save()
                if fav_type == '1':
                    video = Video.objects.get(id=fav_id)
                    video.hav_num += 1
                    if video.hav_num < 0:
                        video.hav_num = 0
                    video.save()
                elif fav_type == '2':
                    user = VideoStar.objects.get(id=fav_id).user
                    user.fans += 1
                    if user.hav_num < 0:
                        user.hav_num = 0
                    user.save()
                return JsonResponse({
                    'status': 'success',
                    'msg': '取消追番'
                })
        else:
            return JsonResponse({
                'status': 'fail',
                'msg': '参数错误'
            })


