from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms

from django.forms.widgets import PasswordInput, TextInput


class CreateUserForm(UserCreationForm):

    """
    Custom form to create/register a user.
    """

    class Meta:
        model = User

        fields = ["username", "email", "password1", "password2"]


class LoginForm(AuthenticationForm):
    """
    Custom form to authenticate a user.
    """

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())
