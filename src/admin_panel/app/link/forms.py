# from django.contrib.postgres.forms import JSONField
from django.forms import ModelForm

from admin_panel.model import useful_link


class LinkForm(ModelForm):
    class Meta:
        model = useful_link.UsefulLink
        fields = '__all__'
