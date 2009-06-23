from django import forms

class PostMessageForm(forms.Form):
    message = forms.CharField(max_length=140)
