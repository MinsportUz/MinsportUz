from django import forms

from admin_panel.model import user, territorial


# class CreateCustomUserForm(forms.ModelForm):
#
#     username = forms.CharField(widget=forms.TextInput(), required=True)
#     phone = forms.CharField(widget=forms.NumberInput(), required=True)
#     password = forms.CharField(widget=forms.PasswordInput(), required=True, min_length=8)
#     email = forms.CharField(widget=forms.EmailInput(), required=False)
#     image = forms.ImageField(widget=forms.FileInput(), required=False)
#     is_superuser = forms.BooleanField(required=False)
#     region = forms.ModelChoiceField(queryset=territorial.Region.objects.all(), required=True)
#
#
#     class Meta:
#         model = user.CustomUser
#         fields = [
#             'user',
#             'phone',
#             'region',
#             'email',
#             'image',
#             'username',
#             'password',
#             'is_superuser',
#         ]

class CreateCustomUserForm(forms.ModelForm):
    class Meta:
        model = user.CustomUser
        fields = '__all__'



