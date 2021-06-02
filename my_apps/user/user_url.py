from django.urls import path
from .views import UserView, ReView, LoginView, LogoutView, SendEmailView, ActiveUserView,IndexView,RecordView,FollowView

urlpatterns = [
    path('user/', UserView.as_view(), name='user'),
    path('re/', ReView.as_view(), name='re'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('re/email', SendEmailView.as_view(), name='re_email'),
    path('active/<str:active_code>', ActiveUserView.as_view(), name='active_code'),
    path('index/', IndexView.as_view(), name='index'),
    path('record/', RecordView.as_view(), name='record'),
    path('follow/', FollowView.as_view(), name='follow')
]
