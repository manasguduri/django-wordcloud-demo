from django import forms
from django.core.validators import URLValidator


class WordcloudForm(forms.Form):
    target_url = forms.URLField(
        max_length=200,
        label='Please enter a url',
        initial='http://',
        validators=[URLValidator(schemes=['http', 'https'])]
    )
