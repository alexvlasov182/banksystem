from django import forms
from django.core.exceptions import ValidationError
from .models import Branch, Customer, Bank


class BranchForm(forms.ModelForm):
    """
    Form for adding or updating a bank branch.
    """

    class Meta:
        model = Branch
        fields = [
            "branch_name",
            "address",
            "branch_code",
        ]
        labels = {
            "branch_name": "Branch Name",
            "address": "Branch Address",
            "branch_code": "Branch Code",
        }

        def clean_branch_code(self):
            branch_code = self.cleaned_data["branch_code"]
            if not branch_code.isalnum():
                raise ValidationError(
                    "Branch code must contain only alphanumeric charcters."
                )
            return branch_code


class CustomerForm(forms.ModelForm):
    """
    Form for adding or updating a customer.
    """

    class Meta:
        model = Customer
        fields = [
            "first_name",
            "last_name",
            "email",
            "age",
        ]
        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email Address",
            "age": "Age",
        }

        def clean_age(self):
            age = self.cleaned_data["age"]
            if age < 18:
                raise ValidationError("Age must be 18 years or older.")
            return age


class BankForm(forms.ModelForm):
    """
    Form for adding or updating a bank
    """

    class Meta:
        model = Bank
        fields = "__all__"
        labels = {"bank_name": "Bank Name", "bank_branch": "Bank Branch"}

    def clean(self):
        cleaned_data = super().clean()
        bank_name = cleaned_data.get("bank_name")
        bank_branch = cleaned_data.get("bank_branch")
        if bank_name and bank_branch and len(bank_name) <= len(bank_branch):
            raise ValidationError(
                f"Bank name should be longer than bank branch. Got {bank_name}, {bank_branch}"
            )
