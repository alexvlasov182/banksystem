from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import BankAccount


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


class CreateAccountForm(forms.Form):
    account_number = forms.CharField(max_length=20, label="Account Number")
    initial_balance = forms.DecimalField(
        max_digits=10, decimal_places=2, label="Initial Balance"
    )

    def clean_account_number(self):
        account_number = self.cleaned_data["account_number"]
        if BankAccount.objects.filter(account_number=account_number).exists():
            raise forms.ValidationError("Account number already exists.")
        return account_number


class ListAccountsForm(forms.Form):
    pass


class ShowBalanceForm(forms.Form):
    pass


class WithdrawForm(forms.Form):
    pass


class DepositForm(forms.Form):
    pass
