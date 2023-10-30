from django.shortcuts import render
from django.http import Http404

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Branch, Bank, Client, Account
from .serializers import BranchSerializer, BankSerializer, AccountSerializer


class BranchesAPIView(generics.ListCreateAPIView):
    """
    List and create branches.

    Attributes:
        queryset: A queryset of all Branch objects.
        serializer_class: The serializer class for Branch objects.
    """

    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class BranchDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrive, update, or delete a specific branch.

    Attributes:
        queryset: A queryset of all Branch objects.
        serializer_class: The serializer class for Branch objects.
    """

    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class BanksAPIView(generics.ListCreateAPIView):
    """
    List and create banks.

    Attributes:
        queryset: A queryset of all Bank objects.
        serializer_class: The serializer class for Bank objects.
    """

    queryset = Bank.objects.all()
    serializer_class = BankSerializer


class BankDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrive, update, or delete a specific bank.

    Attributes:
        queryset: A queryset of all Bank objects.
        serializer_class: The serializer class for Bank objects.
    """

    queryset = Bank.objects.all()
    serializer_class = BankSerializer


class CreateAccountAPIView(APIView):
    def post(self, request):
        client = Client.objects.create(
            name=request.data["full_name"], address=request.data["address"]
        )
        bank = Bank.objects.get(pk=request.data["bank"])
        account = Account.objects.create(
            client=client,
            open_date=request.data["open_date"],
            account_type=request.data["account_type"],
            bank=bank,
        )
        serializer = AccountSerializer(account)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
