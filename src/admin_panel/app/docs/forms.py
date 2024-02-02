from django.forms import ModelForm
from admin_panel.model import docs


class DocsForm(ModelForm):
    class Meta:
        model = docs.Docs
        fields = '__all__'


class DocTypeForm(ModelForm):
    class Meta:
        model = docs.DocType
        fields = '__all__'
