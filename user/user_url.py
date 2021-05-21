from django.urls import path
from .views import testView, testViewT

urlpatterns = [
    path('',testView.as_view(),name='test'),
    path('test2/', testViewT.as_view(),name='test2')
]
