from django.shortcuts import render,redirect,reverse
from django.views.generic import View
# Create your views here.


class testView(View):
    temp = 'test.html'

    def get(self,request):
        return render(request,template_name=self.temp)


class testViewT(View):
    temp = 'test2.html'

    def get(self,request):
        data = {}
        data['text'] = '这是一个测试'
        return render(request, self.temp ,data)