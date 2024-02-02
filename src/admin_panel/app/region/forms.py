from django.forms import ModelForm

from admin_panel.model import territorial


class RegionForm(ModelForm):
    class Meta:
        model = territorial.Region
        fields = '__all__'


