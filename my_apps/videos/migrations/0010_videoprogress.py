# Generated by Django 3.1.3 on 2021-05-28 18:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('videos', '0009_auto_20210525_1055'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoProgress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('modify_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('sub', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_pro_sub', to='videos.videosub', verbose_name='集数')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_pro_user', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_progress', to='videos.video', verbose_name='视频')),
            ],
            options={
                'verbose_name': '观看视频进度',
                'verbose_name_plural': '观看视频进度',
            },
        ),
    ]