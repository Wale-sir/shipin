# Generated by Django 3.1.3 on 2021-05-29 23:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('videos', '0013_auto_20210529_2249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videohistory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_his_user', to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.AlterField(
            model_name='videohistory',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_history', to='videos.video', verbose_name='视频'),
        ),
    ]
