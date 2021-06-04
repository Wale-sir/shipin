from django.shortcuts import render, redirect, reverse, HttpResponse
from django.views.generic import View
from my_apps.user.models import UserProfile, UserFavorite
from .models import Video, VideoSub, VideoComment, VideoStar, VideoHistory
from .forms import VideoHistoryForm, CommentForm
from django.http import JsonResponse
from datetime import datetime
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from my_apps.user.forms import LoginForm, Reform
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


class HomeView(View):
    """主页 显示所有视频"""
    def get(self, request):
        data = {}
        if request.user.is_authenticated:
            user = UserProfile.objects.get(
                username=request.user
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

        return render(request, 'home.html', data)


class VideoDetailView(View):
    """视频观看页"""
    def get(self, request, video_id):
        data = {}

        # 判定是否登陆
        data['user_is_au'] = request.user.is_authenticated
        data['user'] = request.user.id
        # 获取视频
        video = Video.objects.get(id=video_id)
        data['video'] = video

        video.mood += 1
        video.save()
        # 获取集数
        video_sub_number = request.GET.get('video_sub_number')

        # 获取这个视频的某一集
        data['video_sub'] = VideoSub.objects.get(video=video, number=video_sub_number)

        # 收藏状态
        fav_video = False
        # 存储观看记录
        if data['user_is_au']:
            self.history_save(request.user,video=video,sub=video_sub_number)
            if UserFavorite.objects.filter(user=request.user,fav_id=video.id,fav_type='1'):
                fav_video = True
        data['fav_video'] = fav_video

        # 获取这个视频的所有集数
        data['all_video_subs'] = VideoSub.objects.filter(video=video_id)

        # 这个视频的所有评论
        all_comments = VideoComment.objects.filter(video=video, video_sub__number=video_sub_number)
        data['all_comments'] = all_comments

        # 这个视频的所有演员
        data['all_stars'] = VideoStar.objects.filter(video=video_id)

        return render(request, 'video_detail.html',data)

    def history_save(self, user, video, sub):
        """视频记录存储"""
        vid_hty = VideoHistory.objects.filter(user=user, video=video, sub=sub)
        if vid_hty:
            vid_hty.modify_time = datetime.now()
        else:
            VideoHistory.objects.create(user=user,video=video, sub=sub)


class AddComment(View):
    """用户评论功能"""
    def post(self,request):
        if not request.user.is_authenticated:
            return JsonResponse({
                'status': 'fail',
                'msg': '用户未登录'
            })
        video = Video.objects.get(id=request.POST.get('video'))
        video_sub = VideoSub.objects.filter(video=video, number=request.POST.get('video_sub'))
        comment = request.POST.get('comment')
        VideoComment.objects.create(
            user=request.user,
            video=video,
            video_sub=video_sub[0],
            comment=comment
        ).save()

        return JsonResponse({
            'status': 'success',
            'msg': 'ok'
        })


class SearchView(View):

    def get(self,request):
        keyword = request.GET.get('keyword','')
        if keyword == '':
            return redirect(reverse('home'))

        data = {}
        if request.user.is_authenticated:
            user = UserProfile.objects.get(
                username=request.user
            )
            data['username'] = user.username
        data['user_is_au'] = request.user.is_authenticated
        data['login_form'] = LoginForm()
        video_list = Video.objects.filter(name__icontains=keyword).order_by('-start_time')

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(video_list, per_page=20, request=request)
        all_video = p.page(page)

        data['all_video'] = all_video

        return render(request, 'home.html', data)