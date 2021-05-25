from django.db import models
from django.contrib.auth.models import AbstractUser
from my_apps.videos.models import BaseModel
# Create your models here.


GENDER_CHOICE = (
    ('male','男'),
    ('female','女')
)


class UserProfile(AbstractUser):
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
        upload_to='head_image/%Y/%m',
        default='default.jpg'
    )

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.nick_name:
            return self.nick_name
        else:
            return self.username


class UserFavour(BaseModel):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        related_name='user_favour',
        verbose_name='用户'
    )


    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name