from django.shortcuts import render, redirect, reverse, HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.views.generic import View
from .models import UserProfile, EmailPro, UserFavorite, UserMessage
from .forms import Reform, LoginForm, SendEmailForm, AddFavForm, ChangePicForm, ChangeInfoForm,\
    ChangePasswordForm, VideoUploadForm, VideoForm
from django.contrib.auth import login, logout, authenticate
from my_apps.videos.models import Video, VideoHistory, VideoStar
from utils.send_email import send_register_email, random_str
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
from django.contrib.auth.hashers import check_password,make_password
from datetime import datetime
# Create your views here.


class UserView(View):
    """用户界面"""
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('home'))
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
                star = UserProfile.objects.get(id=fav.fav_id)
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
                star = UserProfile.objects.get(id=fav.fav_id)
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
    """更改密码"""
    def post(self, request):
        form = ChangePasswordForm(request.POST)
        data = {}
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            new_check_password = form.cleaned_data['new_check_password']
            user = UserProfile.objects.get(id=request.user.id)
            if not check_password(old_password, user.password):
                data['user_error'] = '旧密码与原密码不一致'
                return render(request,'user.html',data)
            #  更改密码
            user.password = make_password(new_password)
            user.save()
            logout(request)
            return redirect(reverse('home'))
        return render(request, 'user.html', {'user_error': BeautifulSoup(str(form.non_field_errors()), 'lxml').text})


class UserVideoView(View):
    """用户发布视频页"""
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('home'))
        data = {}
        data['user_is_au'] = request.user.is_authenticated
        data['user_video'] = Video.objects.filter(user=request.user)
        return render(request, 'user_video.html', data)

    def post(self,request):
        video_form = VideoForm(request.POST, request.FILES, instance=request.user)
        sub_form = VideoUploadForm(request.POST, request.FILES, instance=request.user)

        if video_form.is_valid() and sub_form.is_valid():
            name = video_form.cleaned_data['name']
            image = video_form.cleaned_data['image']
            info = video_form.cleaned_data['info']

            field = sub_form.cleaned_data['user_field']

            # 先保存视频, 再用sub保存文件   15为用户发布视频
            video = Video.objects.create(user=request.user, name=name, image=image, info=info, start_time=datetime.now(), video_type='15')
            video.video_sub.create(
                video=video,
                user_field=field
            )
            video.save()
            return redirect(reverse('user_video'))
        return render(request,'user_video.html', {'video_error': '发布失败'})


class UserVideoDeleteView(View):
    """用户删除个人视频"""
    def post(self, request):
        video_id = request.POST.get('video_id')
        if video_id:
            video = Video.objects.get(id=video_id)
            video.delete()
            return JsonResponse({
                'status': 'success',
                'msg': '删除成功'
            })
        return JsonResponse({
            'status': 'fail',
            'msg': '参数错误'
        })


class UserMessageView(View):
    """用户消息"""
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('home'))
        data = {}
        data['user_is_au'] = request.user.is_authenticated
        data['user_video'] = Video.objects.filter(user=request.user)
        data['all_message'] = UserMessage.objects.filter(to_user=request.user).order_by('-add_time')
        return render(request, 'user_message.html', data)

    def post(self, request):
        msg_id = request.POST.get('message_id')
        if msg_id:
            msg = UserMessage.objects.get(id=msg_id)
            msg.has_read = True
            msg.save()
            return JsonResponse({
                'status': 'success',
                'msg': '已读'
            })
        return JsonResponse({
            'status': 'fail',
            'msg': '参数错误'
        })


class UserMessageDeleteView(View):
    """用户消息删除"""
    def post(self, request):
        message_id = request.POST.get('message_id')
        if message_id:
            msg = UserMessage.objects.get(id=message_id)
            msg.delete()
            return JsonResponse({
                'status': 'success',
                'msg': '删除成功'
            })
        return JsonResponse({
            'status': 'fail',
            'msg': '参数错误'
        })


class UserHistory(View):
    """用户历史界面"""
    def get(self,request):
        if not request.user.is_authenticated:
            return redirect(reverse('home'))
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


class UserDeleteHistoryView(View):
    """用户删除历史记录"""
    def post(self, request):
        his_id = request.POST.get('his_id')
        if his_id:
            VideoHistory.objects.get(id=his_id).delete()
            return JsonResponse({
                'status': 'success',
                'msg': '删除成功'
            })
        return JsonResponse({
            'status': 'fail',
            'msg': '参数错误'
        })


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
    """修改个人信息"""
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


class DetailUserView(View):
    """用户详情页面"""
    def get(self, request):
        data={}
        data['user_is_au'] = request.user.is_authenticated

        user_id = request.GET.get('user_id')
        user = UserProfile.objects.get(id=user_id)
        data['user'] = user

        # 获取这个用户的所有视频发布
        all_video = Video.objects.filter(user=user)
        data['all_video'] = all_video

        fav_user = False
        if data['user_is_au']:
            if UserFavorite.objects.filter(user=request.user, fav_id=user.id, fav_type='2'):
                fav_user = True
        data['fav_user'] = fav_user

        return render(request, 'detail_user.html', data)


class SendMessageView(View):
    """发送私信"""
    def post(self, request):
        msg = request.POST.get('message')
        user_id = request.GET.get('user_id')
        page = request.GET.get('page')

        if user_id and msg:
            user = UserProfile.objects.get(id=user_id)
            UserMessage.objects.create(user=request.user,to_user=user, title='用户:{}发送'.format(request.user.username), message=msg)

            data = {}
            data['user_is_au'] = request.user.is_authenticated
            user_id = request.GET.get('user_id')
            user = UserProfile.objects.get(id=user_id)
            data['user'] = user

            # 获取这个用户的所有视频发布
            all_video = Video.objects.filter(user=user)
            data['all_video'] = all_video
            if page == 'user_msg':
                return redirect(reverse('user_message'))
            return render(request, 'detail_user.html', data)
        return JsonResponse({
            'status': 'fail',
            'msg': '参数错误'
        })


class ReView(View):
    """注册界面"""

    def post(self, request):
        re_form = Reform(request.POST)
        data={}
        if not re_form.is_valid():
            data['error'] = BeautifulSoup(str(re_form.non_field_errors()), 'lxml').text
            return render(request, 'home.html', data)

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

    def post(self, request):
        form = LoginForm(request.POST)

        data = {}
        if not form.is_valid():
            data['error'] = BeautifulSoup(str(form.non_field_errors()),'lxml').text
            return render(request,'home.html', data)
        login(request, form.cleaned_data.get('user'))

        if request.user.is_authenticated:
            user = UserProfile.objects.get(
                username=request.user.username
            )
            data['username'] = user.username
        data['user_is_au'] = request.user.is_authenticated
        data['login_form'] = LoginForm()
        video_list = Video.objects.all().order_by('-start_time')

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(video_list, per_page=20, request=request)
        all_video = p.page(page)
        data['all_video'] = all_video

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

        data={}
        if not form.is_valid():
            data['error'] = BeautifulSoup(str(form.non_field_errors()), 'lxml').text
            return render(request, 'home.html', data)

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
        if not request.user.is_authenticated:
            return JsonResponse({
                'status': 'fail',
                'msg': '用户未登录'
            })
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
                num = 0
                if fav_type == '1':
                    video = Video.objects.get(id=fav_id)
                    video.hav_num -= 1
                    if video.hav_num < 0:
                        video.hav_num = 0
                    num = video.hav_num
                    video.save()
                elif fav_type == '2':
                    user = UserProfile.objects.get(id=fav_id)
                    user.fans -= 1
                    num = user.fans
                    user.save()
                return JsonResponse({
                    'status': 'success',
                    'msg': '收藏',
                    'num': num
                })

            else:
                UserFavorite.objects.create(
                        user=user,
                        fav_id=fav_id,
                        fav_type=fav_type
                    ).save()
                num = 0
                if fav_type == '1':
                    video = Video.objects.get(id=fav_id)
                    video.hav_num += 1
                    if video.hav_num < 0:
                        video.hav_num = 0
                    num = video.hav_num
                    video.save()
                elif fav_type == '2':
                    user = UserProfile.objects.get(id=fav_id)
                    user.fans += 1
                    num = user.fans
                    user.save()
                return JsonResponse({
                    'status': 'success',
                    'msg': '取消收藏',
                    'num': num
                })
        else:
            return JsonResponse({
                'status': 'fail',
                'msg': '参数错误'
            })


