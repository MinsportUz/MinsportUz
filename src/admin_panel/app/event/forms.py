from django.forms import ModelForm

from admin_panel.model import event


class EventForm(ModelForm):
    class Meta:
        model = event.Event
        fields = '__all__'