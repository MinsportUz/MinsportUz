from django.forms import ModelForm
from admin_panel.model import vacancy


class VacancyForm(ModelForm):
    class Meta:
        model = vacancy.Vacancy
        fields = '__all__'
