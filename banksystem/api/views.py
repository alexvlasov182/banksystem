from django.shortcuts import render
from django.http import Http404

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Branch, Bank
from .serializers import BranchSerializer, BankSerializer


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
