from django.contrib import admin
from .models import Video, VideoSub, VideoStar, VideoComment

# Register your models here.


class VideoAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'video_type', 'nationality_type', 'info',
                    'mood', 'hav_num', 'status', 'start_time', 'image']
    search_fields = ['user', 'name']
    list_filter = ['video_type', 'nationality_type', 'status']


class VideoSubAdmin(admin.ModelAdmin):
    list_display = ['video', 'number', 'likes', 'url']
    search_fields = ['video']
    list_filter = ['video']


class VideoStarAdmin(admin.ModelAdmin):
    list_display = ['video', 'name']
    search_fields = ['video', 'name']
    list_filter = ['video', 'name']


class VideoCommentAdmin(admin.ModelAdmin):
    list_display = ['video', 'video_sub', 'user', 'comment', 'add_time']
    search_fields = ['video', 'user', 'comment']
    list_filter = ['video']


admin.site.register(Video, VideoAdmin)
admin.site.register(VideoSub, VideoSubAdmin)
admin.site.register(VideoStar, VideoStarAdmin)
admin.site.register(VideoComment, VideoCommentAdmin)


