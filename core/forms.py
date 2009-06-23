from django import forms

class PostMessageForm(forms.Form):
    message = forms.CharField(max_length=140)
    reply_id = forms.CharField(max_length=20, required=False, widget=forms.HiddenInput)
