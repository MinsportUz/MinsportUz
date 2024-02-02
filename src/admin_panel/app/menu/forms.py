from django.forms import ModelForm

from admin_panel.model import menu

class MenuForm(ModelForm):
    class Meta:
        model = menu.Menu
        fields = '__all__'