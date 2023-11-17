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
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        return redirect("login")

    accounts = BankAccount.objects.filter(customer=customer)

    show_balance_urls = {}
    for account in accounts:
        account_number = account.account_number
        show_balance_url = reverse(
            "show_balance", kwargs={"account_number": str(account_number)}
        )
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
    account = accounts.filter(account_number=account_number).first()

    if account:
        return render(request, "show_balance.html", {"account": account})
    else:
        return render(request, "account_not_found.html")


@login_required(login_url="/login")
def list_bank_account(request):
    customer = request.user.customer
    accounts = BankAccount.objects.filter(customer=customer)
    return render(request, "list_bank_accounts.html", {"accounts": accounts})


@login_required(login_url="/login")
def withdraw(request, account_number):
    customer = request.user.customer
    accounts = BankAccount.objects.filter(customer=customer)
    account = accounts.filter(account_number=account_number).first()

    if account:
        if request.method == "POST":
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data["amount"]

                if amount > account.balance:
                    return render(
                        request,
                        "withdrawal/withdraw.html",
                        {"form": form, "error_message": "Insufficient funds."},
                    )
                account.balance -= amount
                account.save()

                Transaction.objects.create(
                    bank_account=account,
                    transaction_type="Withdrawal",
                    amount=amount,
                )
                return render(
                    request,
                    "withdrawal/withdraw_success.html",
                    {"account": account, "amount": amount},
                )
        else:
            form = WithdrawForm()

        return render(
            request, "withdrawal/withdraw.html", {"form": form, "account": account}
        )
    elif accounts.count() > 1:
        if request.method == "POST":
            selected_account_number = request.POST.get("account_number")
            selected_account = BankAccount.objects.get(
                customer=customer, account_number=selected_account_number
            )
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data["amount"]

                if amount > selected_account.balance:
                    return render(
                        request,
                        "withdrawal/withdraw.html",
                        {
                            "form": form,
                            "accounts": accounts,
                            "selected_account": selected_account,
                            "error_message": "Insufficient funds.",
                        },
                    )
                selected_account.balance -= amount
                selected_account.save()

                Transaction.objects.create(
                    bank_account=selected_account,
                    transaction_type="Withdrawal",
                    amount=amount,
                )
                return render(
                    request,
                    "withdrawal/withdraw_success.html",
                    {
                        "account": selected_account,
                        "amount": amount,
                        "accounts": accounts,
                    },
                )
        else:
            form = WithdrawForm()
        return render(
            request,
            "withdrawal/choose_account.html",
            {"form": form, "accounts": accounts},
        )
    else:
        return render(request, "withdrawal/no_accounts.html")


@login_required(login_url="/login")
def choose_account(request):
    customer = request.user.customer
    accounts = BankAccount.objects.filter(customer=customer)

    if accounts.count() == 1:
        account_number = accounts.first().account_number
        return redirect("withdraw", account_number=account_number)
    return redirect("withdrawal/choose_account.html", {"accounts": accounts})


@login_required(login_url="/login")
def withdraw_success(request, account_number):
    try:
        account = BankAccount.objects.get(account_number=account_number)
    except BankAccount.DoesNotExist:
        return render(request, "withdraw_fail.html")

    return render(request, "withdraw_success.html", {"account": account})


@login_required(login_url="/login")
def no_accounts(request):
    return render(request, "no_accounts.html")


# Deposit Functionality
@login_required(login_url="/login")
def deposit(request, account_number=None):
    customer = request.user.customer
    accounts = BankAccount.objects.filter(customer=customer)

    if accounts.count() == 1:
        account = accounts.first()
        if request.method == "POST":
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data["amount"]
                account.balance += amount
                account.save()

                Transaction.objects.create(
                    bank_account=account,
                    transaction_type="Deposit",
                    amount=amount,
                )
                return render(
                    request,
                    "deposit/deposit_success.html",
                    {"account": account, "amount": amount},
                )
        else:
            form = DepositForm()

        return render(
            request, "deposit/deposit.html", {"form": form, "account": account}
        )
    elif accounts.count() > 1:
        if request.method == "POST":
            selected_account_number = request.POST.get("account_number")
            selected_account = BankAccount.objects.get(
                customer=customer, account_number=selected_account_number
            )

            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data["amount"]
                selected_account.balance += amount
                selected_account.save()

                Transaction.objects.create(
                    bank_account=selected_account,
                    transaction_type="Deposit",
                    amount=amount,
                )
                return render(
                    request,
                    "deposit/deposit_success.html",
                    {
                        "account": selected_account,
                        "amount": amount,
                        "accounts": accounts,
                    },
                )
        else:
            form = DepositForm()
        return render(
            request,
            "deposit/choose_account_deposit.html",
            {"form": form, "accounts": accounts},
        )
    else:
        return render(request, "deposit/no_accounts_deposit.html")


@login_required(login_url="/login")
def deposit_success(request, account_number=None):
    try:
        account = BankAccount.objects.get(account_number=account_number)
    except BankAccount.DoesNotExist:
        return render(request, "deposit/deposit_fail.html")

    return render(request, "deposit/deposit_success.html", {"account", account})


@login_required(login_url="/login")
def no_accounts_deposit(request):
    return render(request, "deposit/no_accounts_deposit.html")


class CustomLogoutView(LogoutView):
    template_name = "logout.html"
