from decimal import ROUND_HALF_UP, Decimal
from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    """
    Model representing a customer.
    """

    name = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    initial_balance = models.DecimalField(max_digits=10, decimal_places=2)

    """
    String representation of the customer.
    """

    def __str__(self):
        return self.name


class BankAccount(models.Model):
    """
    Model representing a bank account.
    """

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        """
        String representation of the bank account.
        """
        return f"Account {self.account_number} - {self.customer.name}"


class Transaction(models.Model):
    """
    Model representing a transaction.
    """

    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String representation of the transaction.
        """
        rounded_amount = Decimal(str(self.amount)).quantize(
            Decimal("0.00"), rounding=ROUND_HALF_UP
        )
        timestamp_str = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return f"{self.transaction_type} of {rounded_amount} on {timestamp_str}"
