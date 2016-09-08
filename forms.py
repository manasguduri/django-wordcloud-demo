from django import forms


class WordcloudForm(forms.Form):
    target_url = forms.URLField(label='Url')
