from decimal import Decimal, ROUND_HALF_UP
from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from banksystem.models import Customer, BankAccount, Transaction


class CustomerModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.customer = Customer.objects.create(
            name="Test Customer",
            user=self.user,
            address="Test Address",
            phone_number="1234567890",
            initial_balance=100.00,
        )

    def test_customer_str_representation(self):
        """
        Test the string representation of the Customer model.
        """
        expected_str = "Test Customer"
        self.assertEqual(str(self.customer), expected_str)


class BankAccountModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.customer = Customer.objects.create(
            name="Test Customer",
            user=self.user,
            address="Test Address",
            phone_number="1234567890",
            initial_balance=100.00,
        )
        self.bank_account = BankAccount.objects.create(
            customer=self.customer, account_number="123456789", balance=50.00
        )

    def test_bank_account_str_representation(self):
        """
        Test the string representation of the BankAccount model.
        """
        expected_str = f"Account 123456789 - Test Customer"
        self.assertEqual(str(self.bank_account), expected_str)


class TransactionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.customer = Customer.objects.create(
            name="Test Customer",
            user=self.user,
            address="Test Address",
            phone_number="1234567890",
            initial_balance=100.00,
        )
        self.bank_account = BankAccount.objects.create(
            customer=self.customer, account_number="123456789", balance=50.00
        )
        self.transaction = Transaction.objects.create(
            bank_account=self.bank_account, transaction_type="Deposit", amount=25.00
        )

    def test_transaction_str_representation(self):
        """
        Test the string representation of the Transaction model.
        """
        # Create a Transaction with a specific amount
        amount = Decimal("25.00")
        transaction = Transaction.objects.create(
            bank_account=self.bank_account, transaction_type="Deposit", amount=amount
        )

        # Create the expected string representation
        expected_str = f"Deposit of {amount:.2f} on {transaction.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

        # Compare the entire string representation
        self.assertEqual(str(transaction), expected_str)
