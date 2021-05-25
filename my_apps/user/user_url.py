from django.urls import path
from .views import UserView, ReView, LoginView, LogoutView

urlpatterns = [
    path('user', UserView.as_view(), name='user'),
    path('re', ReView.as_view(), name='re'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout')
]
