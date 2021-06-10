from django.db import models
from my_apps.user.models import BaseModel, UserProfile

# Create your models here.


"""
视频
"""

"""视频类别"""

video_type = (
    ('1', '热血'),
    ('2', '冒险'),
    ('3', '搞笑'),
    ('4', '运动'),
    ('5', '竞技'),
    ('6', '剧情'),
    ('7', '穿越'),
    ('8', '青春'),
    ('9', '小说改'),
    ('10', '后宫'),
    ('11', '校园'),
    ('12', '励志'),
    ('13', '恋爱'),
    ('14', '百合'),
    ('15', '用户视频')
)

nation_type = (
    ('1', '中国'),
    ('2', '日本'),
    ('3', '韩国'),
    ('4', '其他')
)


class Video(BaseModel):
    """
    视频信息
    普通视频表(管理员用来上传)
    """
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        related_name='video',
        blank=True,
        null=True,
        verbose_name='用户'
    )
    name = models.CharField(max_length=100,
                            verbose_name='视频名',
                            null=False)
    image = models.ImageField(upload_to='video_image/%Y/%m',
                              verbose_name='封面')
    video_type = models.CharField(max_length=100,
                                  choices=video_type,
                                  verbose_name='视频类别',blank=True,null=True)
    nationality_type = models.CharField(max_length=100,
                                        choices=nation_type,
                                        verbose_name='国家',blank=True,null=True)
    info = models.TextField(verbose_name='简介')
    mood = models.IntegerField(default=0,
                               verbose_name='人气')
    hav_num = models.IntegerField(default=0,
                                  verbose_name='收藏数')
    is_good = models.BooleanField(default=False, verbose_name='是否为精品')
    status = models.BooleanField(default=True,
                                 verbose_name='是否可以观看')
    start_time = models.DateTimeField(verbose_name='开播')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '视频信息'
        verbose_name_plural = verbose_name


class VideoStar(BaseModel):
    """声优"""
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='video_star_user',
        verbose_name='用户',
        blank=True,
        null=True,
    )
    video = models.ForeignKey(
        Video,
        related_name='video_star',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='视频'
    )
    name = models.CharField(max_length=100, null=False, verbose_name='名字')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '声优'
        verbose_name_plural = verbose_name


class VideoSub(BaseModel):
    """集数"""
    video = models.ForeignKey(
        Video,
        related_name='video_sub',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='视频'
    )
    url = models.CharField(max_length=2000, null=True, blank=True, verbose_name='地址')
    number = models.IntegerField(default=1, verbose_name='集数')
    likes = models.IntegerField(default=0, verbose_name='点赞数')

    # 增加1个字段用户上传时 使用
    user_field = models.FileField(blank=True,
                                  null=True,
                                  upload_to='video/%Y/%m',
                                  verbose_name='视频文件(用户上传使用)')

    def __str__(self):
        return '{}'.format(self.number)

    class Meta:
        verbose_name = '集数'
        verbose_name_plural = verbose_name


class VideoComment(BaseModel):
    """用户评论"""
    video = models.ForeignKey(
        Video,
        related_name='video_comment',
        on_delete=models.CASCADE,
        verbose_name='视频',
        blank=True,
        null=True
    )
    video_sub = models.ForeignKey(
        VideoSub,
        related_name='video_sub_comment',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='视频集数'
    )
    user = models.ForeignKey(
        UserProfile,
        related_name='video_user_comment',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='用户'
    )
    to_user = models.ForeignKey(
        UserProfile,
        related_name='to_user',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    comment = models.TextField(verbose_name='用户评论')
    add_time = models.DateTimeField(
        verbose_name='添加时间',
        auto_now=True
    )

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = '视频评论'
        verbose_name_plural = verbose_name


class VideoHistory(BaseModel):
    """视频播放历史"""
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        related_name='video_history',
        verbose_name='视频'
    )
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='video_his_user',
        verbose_name='用户'
    )
    sub = models.IntegerField(
        default=1,
        verbose_name='集数'
    )

    def __str__(self):
        return self.video.name

    class Meta:
        verbose_name = '历史记录'
        verbose_name_plural = verbose_name
