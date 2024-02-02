from django.forms import ModelForm

from admin_panel.model import territorial


class DistrictForm(ModelForm):
    class Meta:
        model = territorial.District
        fields = '__all__'


