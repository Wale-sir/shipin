from django import forms
from .models import VideoHistory, VideoComment


class VideoHistoryForm(forms.ModelForm):

    class Meta:
        model = VideoHistory
        fields =['video','sub']


class CommentForm(forms.ModelForm):
    class Meta:
        model = VideoComment
        fields = ['video','video_sub','comment']
