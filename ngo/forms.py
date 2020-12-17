from django import forms
from .models import Subscriber
from vauth.models import Applicant
from django.forms import ModelForm
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField(widget=forms.NumberInput())
    message = forms.CharField(widget=forms.TextInput())

SEX = (
    ('male','male'),
    ('female', 'female')
)

class ApplicantForm(ModelForm):
    sex = forms.ChoiceField(choices=SEX)
    class Meta:
        model = Applicant
        exclude = ['date_applied']
        error_messages = {
            'email': {
                'unique': _("Sorry Someone has already applied using this email."),
            },
        }

class SubscriberForm(ModelForm):
    class Meta:
        model = Subscriber
        fields = '__all__'
        