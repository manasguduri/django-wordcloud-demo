from django import forms
from django.forms.widgets import TextInput


class WordcloudForm(forms.Form):
    target_url = forms.URLField(
        max_length=200,
        label='Please enter a url',
        initial='http://',
        widget=TextInput({'class': 'form-control'})
    )
