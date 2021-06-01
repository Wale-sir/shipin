# Generated by Django 3.1.3 on 2021-05-25 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0007_auto_20210525_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='videocomment',
            name='video_sub',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='video_sub_comment', to='videos.videosub', verbose_name='视频集数'),
        ),
        migrations.AlterField(
            model_name='videocomment',
            name='video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='video_comment', to='videos.video'),
        ),
    ]
