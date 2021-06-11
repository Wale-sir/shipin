from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


GENDER_CHOICE = (
    ('male', '男'),
    ('female', '女')
)
FAV_TYPE = (
    ('1', '视频'),
    ('2', '用户'),
)


class BaseModel(models.Model):
    #  基类 不生成表
    add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    modify_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    class Meta:
        abstract = True


class UserProfile(AbstractUser):
    """用户信息"""
    nick_name = models.CharField(
        max_length=30,
        verbose_name='昵称',
        default=''
    )
    birthday = models.DateTimeField(
        verbose_name='生日',
        null=True,
        blank=True
    )
    gender = models.CharField(
        choices=GENDER_CHOICE,
        verbose_name='性别',
        max_length=6
    )
    address = models.CharField(
        verbose_name='地址',
        max_length=200,
        default=''
    )
    mobile = models.CharField(
        verbose_name='手机号码',
        max_length=20
    )
    image = models.ImageField(
        verbose_name='头像',
        upload_to=r'head_image/%Y/%m',
        default='default.jpg'
    )
    fans = models.IntegerField(default=0,
                               verbose_name='收藏数')

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.nick_name:
            return self.nick_name
        else:
            return self.username


class UserFavorite(BaseModel):
    """用户收藏"""
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        verbose_name='用户'
    )
    fav_id = models.IntegerField(
        verbose_name='数据id'
    )

    fav_type = models.CharField(
        default='1',
        max_length=5,
        choices=FAV_TYPE,
        verbose_name='收藏类型'
    )

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{username}_{fav_id}'.format(username=self.user.username, fav_id=self.fav_id)


class UserMessage(BaseModel):
    """用户消息"""
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        verbose_name='用户'
    )
    title = models.CharField(
        default='title',
        max_length=50,
        verbose_name='标题'
    )
    message = models.CharField(
        max_length=200,
        verbose_name='消息内容'
    )
    has_read = models.BooleanField(
        default=False,
        verbose_name='是否已读'
    )

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.message


# 邮箱--用来激活账号和找回密码
class EmailPro(BaseModel):
    code = models.CharField(max_length=20, verbose_name='验证码')
    email = models.EmailField(max_length=50, verbose_name='邮箱')
    send_type = models.CharField(max_length=10, choices=(('register', '邮箱注册'), ('forget', '忘记密码')), verbose_name='发送类型')
    send_time = models.DateTimeField(auto_now_add=True, verbose_name='发送时间')

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name
