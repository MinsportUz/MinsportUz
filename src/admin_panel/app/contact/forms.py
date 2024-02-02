from django.forms import ModelForm

from admin_panel.model import contact


class ContactForm(ModelForm):
    class Meta:
        model = contact.Contact
        fields = '__all__'


class FeedbackForm(ModelForm):
    class Meta:
        model = contact.Feedback
        fields = '__all__'


class ReceptionForm(ModelForm):
    class Meta:
        model = contact.Reception
        fields = '__all__'
