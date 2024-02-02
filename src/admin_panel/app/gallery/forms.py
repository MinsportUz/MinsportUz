from django.forms import ModelForm
from admin_panel.model import press_service


class PhotoForm(ModelForm):
    class Meta:
        model = press_service.PhotoGallery
        fields = '__all__'


class VideoForm(ModelForm):
    class Meta:
        model = press_service.VideoGallery
        fields = '__all__'
