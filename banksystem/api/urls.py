from django.urls import path

from .views import (
    BranchesAPIView,
    BanksAPIView,
    BranchDetailAPIView,
    BankDetailAPIView,
    CreateAccountAPIView,
    AccountListAPIView,
    DepositAPIView,
    WithdrawAPIView,
    AccountDetailAPIView,
)

app_name = "banksystem"

urlpatterns = [
    # List and create branches
    path("branches/", BranchesAPIView.as_view(), name="branch-list"),
    # Retrive, update, or delete a specific branch
    path("branch/<int:pk>/", BranchDetailAPIView.as_view(), name="branch-detail"),
    # List and create banks
    path("banks/", BanksAPIView.as_view(), name="bank-list"),
    # Retrive, update, or delete a specific bank
    path("bank/<int:pk>/", BankDetailAPIView.as_view(), name="bank-detail"),
    # Create account
    path("create_account/", CreateAccountAPIView.as_view(), name="create-account"),
    # Retrive account
    path("accounts/", AccountListAPIView.as_view(), name="accounts"),
    # Create deposit
    path("deposits/", DepositAPIView.as_view(), name="deposits"),
    # Create withdraw
    path("withdrawals/", WithdrawAPIView.as_view(), name="withdrawals"),
    # Get id account
    path("account/<int:pk>/", AccountDetailAPIView.as_view(), name="account-detail"),
]
