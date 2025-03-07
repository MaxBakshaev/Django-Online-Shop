from typing import Any
from django import forms


class SendEmailForm(forms.Form):

    user_name = forms.CharField(max_length=100, min_length=2)
    user_email = forms.EmailField(max_length=50, min_length=4)
    user_subject = forms.CharField(max_length=150)
    user_message = forms.CharField(widget=forms.Textarea, max_length=3000)
    
    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        return cleaned_data
