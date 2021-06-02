from django.urls import path
from .views import HomeView, VideoDetailView

urlpatterns = [
    path('',HomeView.as_view(), name='home'),
    path('video/<int:video_id>/', VideoDetailView.as_view(), name='video_sub')
]