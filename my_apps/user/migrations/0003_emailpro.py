# Generated by Django 3.1.3 on 2021-05-28 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_userfavorite_usermessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailPro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('modify_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('code', models.CharField(max_length=20, verbose_name='验证码')),
                ('email', models.EmailField(max_length=50, verbose_name='邮箱')),
                ('send_type', models.CharField(choices=[('register', '邮箱注册'), ('forget', '忘记密码')], max_length=10, verbose_name='发送类型')),
                ('send_time', models.DateTimeField(auto_now_add=True, verbose_name='发送时间')),
            ],
            options={
                'verbose_name': '邮箱验证码',
                'verbose_name_plural': '邮箱验证码',
            },
        ),
    ]