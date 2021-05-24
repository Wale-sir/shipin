from django.shortcuts import render,redirect,reverse
from django.views.generic import View
from .models import UserProfile
# Create your views here.


class UserView(View):

    def get(self, request):
        return render(request, template_name='user.html')
