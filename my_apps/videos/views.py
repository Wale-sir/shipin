from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from my_apps.user.models import UserProfile
from .models import Video, VideoSub, VideoComment, VideoStar
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
        data['user'] = request.user.is_authenticated

        video_list = Video.objects.all()
        data['video_list'] = video_list
        return render(request, 'home.html', data)


class VideoDetailView(View):
    """视频观看页"""
    def get(self, request, video_id):
        data = {}
        # 判定是否登陆
        data['user'] = request.user.is_authenticated

        # 视频信息
        video_subs = VideoSub.objects.filter(video=video_id)
        data['video_subs'] = video_subs
        video_comments = VideoComment.objects.filter(video=video_id)
        data['video_comments'] = video_comments
        video_stars = VideoStar.objects.filter(video=video_id)
        data['video_stars'] = video_stars
        return render(request, 'video_detail.html',data)