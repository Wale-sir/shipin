# Generated by Django 3.1.3 on 2021-05-28 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_emailpro'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfavorite',
            name='fav_type',
            field=models.CharField(choices=[('1', '视频'), ('2', '演员')], default='1', max_length=5, verbose_name='收藏类型'),
        ),
    ]
