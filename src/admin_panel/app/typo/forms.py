from django.forms import ModelForm

from admin_panel.model.settings import Typo


class TypoForm(ModelForm):
    class Meta:
        model = Typo
        fields = '__all__'
