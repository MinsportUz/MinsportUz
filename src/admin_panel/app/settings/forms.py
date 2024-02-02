from django.contrib.postgres.forms import JSONField
from django.forms import ModelForm

from admin_panel.model.settings import MainPageSetting, ContactSetting


class GeneralSettingForm(ModelForm):
    class Meta:
        model = MainPageSetting
        fields = '__all__'


class ContactSettingForm(ModelForm):
    class Meta:
        model = ContactSetting
        fields = '__all__'
