from django.urls import path
from .views import HomeView, VideoDetailView, AddComment, SearchView, AddLikes

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('video/<int:video_id>', VideoDetailView.as_view(), name='video_detail'),
    path('add_comment/', AddComment.as_view(), name='add_comment'),
    path('search/', SearchView.as_view(), name='search_view'),
    path('add_likes/', AddLikes.as_view(), name='add_likes')
]