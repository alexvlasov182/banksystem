from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import BankAccount


class SignUpForm(UserCreationForm):
    """
    Form for user registration.
    """

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

    """
    Form for user login.
    """

    pass


class CreateAccountForm(forms.Form):
    """
    Form for creating a new bank account.
    """

    account_number = forms.CharField(max_length=20, label="Account Number")
    initial_balance = forms.DecimalField(
        max_digits=10, decimal_places=2, label="Initial Balance"
    )

    def clean_account_number(self):
        """
        Custom validation to check if the account number already exists.
        """
        account_number = self.cleaned_data["account_number"]
        if BankAccount.objects.filter(account_number=account_number).exists():
            raise forms.ValidationError("Account number already exists.")
        return account_number


class WithdrawForm(forms.Form):
    """
    Form for withdrawing money from an account.
    """

    amount = forms.DecimalField(
        label="Withdrawal Amount",
        min_value=0.01,
        widget=forms.NumberInput(attrs={"step": "0.01"}),
    )


class DepositForm(forms.Form):
    """
    Form for depositing money into an account.
    """

    amount = forms.DecimalField(label="Amount", min_value=0.01)
