from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic.edit import FormView
from .forms import (
    SignUpForm,
    LoginForm,
    CreateAccountForm,
    ListAccountsForm,
    ShowBalanceForm,
    WithdrawForm,
    DepositForm,
)
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

    show_balance_urls = {}
    for account in accounts:
        account_number = account.account_number
        show_balance_url = reverse(
            "show_balance", kwargs={"account_number": account_number}
        )
        print(f"Account: {account_number}, URL: {show_balance_url}")
        show_balance_urls[account_number] = show_balance_url

    return render(
        request,
        "dashboard.html",
        {
            "customer": customer,
            "accounts": accounts,
            "show_balance_urls": show_balance_urls,
        },
    )


def homepage(request):
    """
    Render the homepage with the current date
    """
    current_date = timezone.now()
    return render(request, "index.html", {"current_date": current_date})


@login_required(login_url="/login")
def create_account(request):
    if request.method == "POST":
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            account_number = form.cleaned_data["account_number"]
            initial_balance = form.cleaned_data["initial_balance"]

            BankAccount.objects.create(
                customer=request.user.customer,
                account_number=account_number,
                balance=initial_balance,
            )
            return redirect("list_bank_accounts")
    else:
        form = CreateAccountForm()

    return render(request, "create_account.html", {"form": form})


def show_balance(request, account_number):
    customer = request.user.customer
    accounts = BankAccount.objects.filter(customer=customer)

    # Find the account with the specified account_number
    account = accounts.filter(account_number=account_number).first()

    if account:
        # If the account is found, render the balance
        return render(request, "show_balance.html", {"balance": account.balance})
    else:
        # If the account is not found, you might want to handle this case, e.g., redirect or show an error message
        return render(request, "account_not_found.html")


@login_required(login_url="/login")
def list_bank_account(request):
    customer = request.user.customer
    accounts = BankAccount.objects.filter(customer=customer)
    return render(request, "list_bank_accounts.html", {"accounts": accounts})


@login_required(login_url="/login")
def withdraw(request):
    customer = request.user.customer
    accounts = BankAccount.objects.filter(customer=customer)

    # If the customer has only one account, directly show the balance
    if accounts.count() == 1:
        account = accounts.first()
        if request.method == "POST":
            # Handle the withdrawal logic here
            withdrawal_amount = float(request.POST.get("withdrawal_amount", 0))
            if withdrawal_amount > 0 and withdrawal_amount <= account.balance:
                # Withdrawal is valid, update the balance and create a transaction
                account.balance -= withdrawal_amount
                account.save()
                Transaction.objects.create(
                    bank_account=account,
                    transaction_type="Withdrawal",
                    amount=withdrawal_amount,
                )
                return render(
                    request, "withdraw_success.html", {"balance": account.balance}
                )
            else:
                # Invalid withdrawal amount, show an error message
                return render(
                    request,
                    "withdraw_error.html",
                    {"error_message": "Invalid withdrawal amount"},
                )
        else:
            return render(request, "withdraw.html", {"account": account})

    # If the customer has multiple accounts, display a list of accounts
    if request.method == "POST":
        # Handle the form submission to choose an account
        account_number = request.POST.get("account_number")
        selected_account = accounts.filter(account_number=account_number).first()
        if selected_account:
            # Render the withdrawal form for the selected account
            return render(request, "withdraw.html", {"account", selected_account})
        else:
            # Invalid account selection, show an error message
            return render(
                request,
                "withdraw_error.html",
                {"error_message": "Invalid account selection"},
            )
    else:
        return render(request, "choose_account_withdraw.html", {"accounts": accounts})


class CustomLogoutView(LogoutView):
    template_name = "logout.html"
