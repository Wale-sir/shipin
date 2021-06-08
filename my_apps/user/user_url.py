from django.urls import path
from .views import UserView, ReView, LoginView, \
    LogoutView, SendEmailView, ActiveUserView, FavView,\
    UserFavView, UserHistory, ChangePic, ChangeInfo, ChangePassword

urlpatterns = [
    path('user/', UserView.as_view(), name='user'),
    path('user/fav/',UserFavView.as_view(), name='user_fav'),
    path('user/history/', UserHistory.as_view(), name='user_history'),
    path('user/change/pic/', ChangePic.as_view(), name='change_pic'),
    path('user/change/info/', ChangeInfo.as_view(), name='change_info'),
    path('user/change/password', ChangePassword.as_view(), name='change_password'),

    path('re/', ReView.as_view(), name='re'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('re/email/', SendEmailView.as_view(), name='re_email'),
    path('active/<str:active_code>/', ActiveUserView.as_view(), name='active_code'),
    path('fav/', FavView.as_view(), name='add_fav')
]
