from django import forms
from .models import Account


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = [
            "name",
            "photo",
            "phone",
            "email",
            "password",
        ]
