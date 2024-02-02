from django.forms import ModelForm
from admin_panel.model import tender


class TenderForm(ModelForm):
    class Meta:
        model = tender.Tender
        fields = '__all__'
