from django import forms
from .models import VideoHistory


class VideoHistoryForm(forms.ModelForm):

    class Meta:
        model = VideoHistory
        fields =['video','sub']