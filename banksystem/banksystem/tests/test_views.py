from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from banksystem.models import Customer, BankAccount


class TransactionViewsTestCase(TestCase):
    def setUp(self):
        # Create a user and log in
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")

    def test_deposit_view(self):
        url = reverse("deposit")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Add more assertions as needed for the deposit view
