from django import forms
from .models import UserProfile
from django.contrib.auth import authenticate


class Reform(forms.Form):
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
        if password != check_password:
            raise forms.ValidationError('两次密码不一致')

        user = UserProfile.objects.filter(username=username)
        if user:
            raise forms.ValidationError('用户已存在')
        return self.cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput, error_messages={
        'required': '输入用户名'
    })
    password = forms.CharField(required=True, widget=forms.PasswordInput, error_messages={
        'required': '输入密码'
    })

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        user = UserProfile.objects.filter(username=username)
        if not user:
            raise forms.ValidationError('用户不存在')

        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError('密码错误')
        self.cleaned_data['user'] = user
        return self.cleaned_data



