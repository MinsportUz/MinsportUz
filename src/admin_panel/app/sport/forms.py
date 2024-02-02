from django.forms import ModelForm
from admin_panel.model import sport


class StadionForm(ModelForm):
    class Meta:
        model = sport.Stadion
        fields = '__all__'


class TypeForm(ModelForm):
    class Meta:
        model = sport.SportType
        fields = '__all__'


class ChampionForm(ModelForm):
    class Meta:
        model = sport.Champion
        fields = '__all__'
