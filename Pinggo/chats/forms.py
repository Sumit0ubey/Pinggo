from django.forms import ModelForm
from django import forms

from .models import ChatGroup, GroupMessage


class ChatMessageCreateForm(ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['message']
        widgets = {
            'message': forms.TextInput(attrs={'class': 'p-2 text-black', 'autofocus':True, 'placeholder': 'Message here...'}),
        }

