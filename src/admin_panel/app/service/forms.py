from django.forms import ModelForm
from admin_panel.model.ministry import AboutMinistry, MinistryStat, MinistryStructure
# from django.contrib.postgres.forms import JSONField
from admin_panel.model import service


class ServiceForm(ModelForm):
    class Meta:
        model = service.Service
        fields = '__all__'
