from django.forms import ModelForm

from admin_panel.model.static import StaticPage


class StaticForm(ModelForm):
    class Meta:
        model = StaticPage
        fields = '__all__'
