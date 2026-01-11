from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

from .models import Profile

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        widgets = {
            'image': forms.HiddenInput(),
            'displayname': forms.TextInput(attrs={'placeholder': 'Add Display Name'}),
            'info': forms.Textarea(attrs={'placeholder': 'Add Information'}),
        }

class EmailForm(ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email']
