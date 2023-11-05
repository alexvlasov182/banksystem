from django import forms
from .models import Branch, Customer


class BranchForm(forms.ModelForm):
    """
    Form for adding or updating a bank branch.
    """

    class Meta:
        model = Branch
        fields = "__all__"
        labels = {
            "name": "Branch Name",
            "address": "Branch Address",
            "branch_code": "Branch Code",
        }


class CustomerForm(forms.ModelForm):
    """
    Form for adding or updating a customer.
    """

    class Meta:
        model = Customer
        fields = "__all__"
        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email Address",
            "age": "Age",
        }
