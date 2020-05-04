from django.forms import ModelForm
from video.models import VideoFile

class VideoFileForm(ModelForm):
    class Meta:
        model = VideoFile
        fields = ['title', 'date_taken', 'file_obj']