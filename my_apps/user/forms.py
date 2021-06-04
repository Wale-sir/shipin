from django import forms
from .models import UserProfile, UserFavorite
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
import re


class Reform(forms.Form):
    """用户名验证注册"""
    username = forms.CharField(required=True, widget=forms.TextInput,error_messages={
        'required': '用户名必须填写'
    })
    password = forms.CharField(required=True, widget=forms.PasswordInput,error_messages={
        'required': '密码必须填写'
    })
    check_password = forms.CharField(required=True, widget=forms.PasswordInput, error_messages={
        'required': '请重复密码'
    })

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        check_password = self.cleaned_data.get('check_password')

        if len(username) < 5:
            raise forms.ValidationError('用户名过短')
        if len(password) < 6:
            raise forms.ValidationError('密码过短')
        if not username or not password or not check_password:
            raise forms.ValidationError('请填写完整!')
        if password != check_password:
            raise forms.ValidationError('两次密码不一致')

        user = UserProfile.objects.filter(username=username)
        if user:
            raise forms.ValidationError('用户已存在')
        return self.cleaned_data


class SendEmailForm(forms.Form):
    """邮箱验证注册"""
    email = forms.EmailField(required=True, widget=forms.TextInput, error_messages={
        'required': '用户名必须填写'
    })
    password = forms.CharField(required=True, widget=forms.PasswordInput, error_messages={
        'required': '密码必须填写'
    })
    check_password = forms.CharField(required=True, widget=forms.PasswordInput, error_messages={
        'required': '请重复密码'
    })

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        check_password = self.cleaned_data.get('check_password')
        if not re.search(r'[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}', str(email)):
            raise forms.ValidationError('邮箱不合法')

        if len(password) < 6:
            raise forms.ValidationError('密码过短')
        if not email or not password or not check_password:
            raise forms.ValidationError('请填写完整!')
        if password != check_password:
            raise forms.ValidationError('两次密码不一致')

        user = UserProfile.objects.filter(email=email)
        if user:
            raise forms.ValidationError('邮箱已被注册')
        return self.cleaned_data


class LoginForm(forms.Form):
    """登录验证注册"""
    username = forms.CharField(required=True, widget=forms.TextInput, error_messages={
        'required': '输入用户名或邮箱'
    })
    password = forms.CharField(required=True, widget=forms.PasswordInput, error_messages={
        'required': '输入密码'
    })

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        # 验证是否输入
        if not username or not password:
            raise forms.ValidationError('输入用户名或密码')

        #  邮箱验证登录  验证是否符合邮箱
        if re.search(r'[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}', str(username)):

            #  用户邮箱 查找
            all_user = UserProfile.objects.filter(email=username)
            for user in all_user:
                if not user:
                    raise forms.ValidationError('用户不存在')

                if not check_password(password,user.password):
                    raise forms.ValidationError('密码错误')

                self.cleaned_data['user'] = user
                return self.cleaned_data

        #  用户名验证登录
        user = UserProfile.objects.filter(username=username)
        if not user:
            raise forms.ValidationError('用户不存在')

        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError('密码错误')
        self.cleaned_data['user'] = user
        return self.cleaned_data


class AddFavForm(forms.ModelForm):

    class Meta:
        model = UserFavorite
        fields = ['fav_id','fav_type']