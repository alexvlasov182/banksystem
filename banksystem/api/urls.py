from django.urls import path

from .views import BranchesAPIView, BanksAPIView, BranchDetailAPIView, BankDetailAPIView

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
]
