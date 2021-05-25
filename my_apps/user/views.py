from django.shortcuts import render,redirect,reverse
from django.views.generic import View
from .models import UserProfile
from .forms import Reform, LoginForm
from django.contrib.auth import login, logout, authenticate
# Create your views here.


class UserView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        return render(request, 'user.html', {
            'type': 'home'
        })


class ReView(View):
    def get(self,request):
        # form = Reform()
        return render(request,'re.html',{
            # 'form': form
        })

    def post(self, request):
        form = Reform(request.POST)
        if not form.is_valid():
            return render(request,'re.html',{
                'error': form.non_field_errors
            })
        UserProfile.objects.create_user(
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password')
        ).save()
        return redirect(reverse('home'))


class LoginView(View):

    def get(self,request):
        if request.user.is_authenticated:
            return redirect(reverse('home'))
        return render(request,'login.html', {
            'user': request.user.is_authenticated
        })

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.cleaned_data.get('user'))
        else:
            return render(request, 'login.html',{
                'error': form.non_field_errors
            })
        return redirect(reverse('home'))


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect(reverse('home'))