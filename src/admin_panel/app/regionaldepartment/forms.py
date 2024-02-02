from django.forms import ModelForm

from admin_panel.model import territorial



class RegionalDepartmentForm(ModelForm):
    class Meta:
        model = territorial.RegionalDepartment
        fields = '__all__'
