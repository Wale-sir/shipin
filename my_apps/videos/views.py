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
                username=request.user.username
            )
            data['username'] = user.username
        data['user_is_au'] = request.user.is_authenticated
        data['login_form'] = LoginForm()

        all_video = Video.objects.all().exclude(video_type='15')
        # 按条件查询
        category = request.GET.get('ct', '')
        data['category'] = category
        if category:
            all_video = all_video.filter(video_type=category)  # 按类别分

        city = request.GET.get('city','')
        data['city'] = city
        if city:
            all_video = all_video.filter(nationality_type=city)  # 按国家分

        video_list = all_video.order_by('-start_time')

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(video_list, per_page=20, request=request)
        all_video = p.page(page)
        data['all_video'] = all_video

        # 精品视频
        data['good_videos'] = Video.objects.filter(is_good=True)
        # 用户发布视频 15为用户发布视频
        data['user_videos'] = Video.objects.filter(video_type='15')
        return render(request, 'home.html', data)


class VideoDetailView(View):
    """视频观看页"""
    def get(self, request, video_id):
        data = {}

        # 判定是否登陆
        data['user_is_au'] = request.user.is_authenticated
        data['user'] = request.user
        # 获取视频
        video = Video.objects.get(id=video_id)
        data['video'] = video

        video.mood += 1
        video.save()
        # 获取集数
        video_sub_number = request.GET.get('video_sub_number')

        # 获取这个视频的某一集
        try:
            data['video_sub'] = VideoSub.objects.get(video=video, number=video_sub_number)
        except:
            return redirect(reverse('home'))

        # 收藏状态
        fav_video = False
        fav_user = False
        # 存储观看记录
        if data['user_is_au']:
            self.history_save(request.user, video=video,sub=video_sub_number)
            if UserFavorite.objects.filter(user=request.user,fav_id=video.id,fav_type='1'):
                fav_video = True
            if UserFavorite.objects.filter(user=request.user,fav_id=video.user.id,fav_type='2'):
                fav_user = True

        data['fav_user'] = fav_user
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
            VideoHistory.objects.create(user=user, video=video, sub=sub)


class AddLikes(View):
    """视频点赞功能"""
    def post(self, request):
        if request.user.is_authenticated:
            video_sub_id = request.POST.get('video_sub_id')
            if video_sub_id:
                video_sub = VideoSub.objects.get(id=video_sub_id)
                video_sub.likes += 1
                video_sub.save()
                num = video_sub.likes
                return JsonResponse({
                    'status': 'success',
                    'msg': 'ok',
                    'num': num
                })
            return JsonResponse({
                'status': 'fail',
                'msg': '参数错误'
        })
        return JsonResponse({
            'status': 'fail',
            'msg': '用户未登录'
        })


class AddComment(View):
    """用户评论视频功能"""
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
    """搜索功能"""
    def get(self,request):
        keyword = request.GET.get('keyword','')
        if keyword == '':
            return redirect(reverse('home'))

        data = {}
        if request.user.is_authenticated:
            user = UserProfile.objects.get(
                username=request.user.username
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

        return render(request, 'search.html', data)