from django.forms import ModelForm
from admin_panel.model import ministry


class AboutMinistryForm(ModelForm):
    class Meta:
        model = ministry.AboutMinistry
        fields = '__all__'


class MinistryStatForm(ModelForm):
    class Meta:
        model = ministry.MinistryStat
        fields = '__all__'


class MinistryStructureForm(ModelForm):
    class Meta:
        model = ministry.MinistryStructure
        fields = '__all__'


class DepartmentForm(ModelForm):
    class Meta:
        model = ministry.Department
        fields = '__all__'


class OrganizationForm(ModelForm):
    class Meta:
        model = ministry.Organization
        fields = '__all__'


class StaffForm(ModelForm):
    class Meta:
        model = ministry.Staff
        fields = '__all__'
