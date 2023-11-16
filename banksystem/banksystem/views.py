from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from .forms import SignUpForm, LoginForm
from .models import Customer, BankAccount, Transaction

from django.utils import timezone


class SignUpView(FormView):
    form_class = SignUpForm
    template_name = "auth/signup.html"
    success_url = "/login"

    def form_valid(self, form):
        user = form.save()
        customer = Customer.objects.create(
            user=user,
            name=form.cleaned_data["name"],
            address=form.cleaned_data["address"],
            phone_number=form.cleaned_data["phone_number"],
            initial_balance=form.cleaned_data["initial_balance"],
        )
        account = BankAccount.objects.create(
            customer=customer,
            account_number=str(user.id),
            balance=form.cleaned_data["initial_balance"],
        )
        Transaction.objects.create(
            bank_account=account,
            transaction_type="Deposit",
            amount=form.cleaned_data["initial_balance"],
        )
        login(self.request, user)
        return super().form_valid(form)


class CustomLoginView(LoginView):
    form_class = LoginForm


@login_required(login_url="/login")
def customer_dashboard(request):
    customer = request.user.customer
    accounts = BankAccount.objects.filter(customer=customer)
    return render(
        request,
        "dashboard.html",
        {"customer": customer, "accounts": accounts},
    )


def homepage(request):
    """
    Render the homepage with the current date
    """
    current_date = timezone.now()
    return render(request, "index.html", {"current_date": current_date})


class CustomLogoutView(LogoutView):
    template_name = "logout.html"
