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
            "show_balance", kwargs={"account_number": str(account_number)}
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
        return render(request, "show_balance.html", {"account": account})
    else:
        # If the account is not found, you might want to handle this case, e.g., redirect or show an error message
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

    # Find the account with the specified account_number
    account = accounts.filter(account_number=account_number).first()

    # If the customer has only one account, directly show the balance
    if account:
        if request.method == "POST":
            # Handle the withdrawal logic here
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

    # If the customer has multiple accounts, display a list of accounts
    elif accounts.count() > 1:
        if request.method == "POST":
            # Handle the form submission to choose an account
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
        # If there's only one account, directly redirect to withdraw page
        account_number = accounts.first().account_number
        return redirect("withdraw", account_number=account_number)
    return redirect("withdrawal/choose_account.html", {"accounts": accounts})


@login_required(login_url="/login")
def withdraw_success(request, account_number):
    # Retrive the BankAccount object based on the account number
    try:
        account = BankAccount.objects.get(account_number=account_number)
    except BankAccount.DoesNotExist:
        # Handle the case where the account doesn't exist
        return render(request, "withdraw_fail.html")

    return render(request, "withdraw_success.html", {"account": account})


@login_required(login_url="/login")
def no_accounts(request):
    return render(request, "no_accounts.html")


class CustomLogoutView(LogoutView):
    template_name = "logout.html"
