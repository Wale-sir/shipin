from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from my_apps.user.models import UserProfile
# Create your views here.


class HomeView(View):

    def get(self, request):
        data = {}
        if request.user.is_authenticated:
            user = UserProfile.objects.get(
                username=request.user
            )
            data['username'] = user.username
        data['user'] = request.user.is_authenticated
        return render(request, 'home.html', data)