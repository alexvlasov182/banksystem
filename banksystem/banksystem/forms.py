from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=255)
    address = forms.CharField(widget=forms.Textarea)
    phone_number = forms.CharField(max_length=15)
    initial_balance = forms.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = User
        fields = [
            "name",
            "address",
            "phone_number",
            "username",
            "initial_balance",
            "password1",
            "password2",
        ]


class LoginForm(AuthenticationForm):
    pass
