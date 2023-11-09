from django import forms
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


class BankForm(forms.ModelForm):
    """
    Form for adding or updating a bank
    """

    class Meta:
        model = Bank
        fields = "__all__"
        labels = {"bank_name": "Bank Name", "bank_branch": "Bank Branch"}
