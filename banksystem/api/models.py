from __future__ import unicode_literals
from django.db import models


class Branch(models.Model):

    """
    Represent a bank branch

    Attributes:
        name (str): The name of the branch.
        address (str): The address of the branch.
        branch_code (str): The branch code.

    Meta:
        verbose_name_plural = "Branches"
    """

    name = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    branch_code = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    def to_json(self):
        """Converts the Branch instance to a JSON-like object."""
        return {
            "name": self.name,
            "address": self.address,
            "branch_code": self.branch_code,
        }


class Bank(models.Model):

    """
    Represent a bank.

    Attributes:
        name (str): The name of the bank.
        branch (Branch): The branch to which the bank belongs.
    """

    name = models.CharField(max_length=250)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def to_json(self):
        return {
            "name": self.name,
            "branch": self.branch.to_json(),
        }


class ClientManager(models.Model):

    """
    Represent a client mananger.

    Attributes:
        name (str): The name of the client manager.
    """

    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Client(models.Model):

    """
    Represent a client.

    Attributes:
        name (str): The name of the client.
        address (str): The addres of the client.
    """

    name = models.CharField(max_length=250)
    address = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    def to_json(self):
        """Converts the Client instance to a JSON-like object."""
        return {"name": self.name, "address": self.address}


class Account(models.Model):
    """
    Represent a bank account

    Attributes:
        client (Client): The client associated with the account.
        open_date (str): The date the account was opened.
        account_type (str): The type of the account.
        bank (Bank): The bank to which the account belongs.
    """

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    open_date = models.CharField(max_length=250)
    account_type = models.CharField(max_length=250)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)

    def __str__(self):
        return self.account_type

    def to_json(self):
        """Converts the Account instance to a JSON-like object"""
        return {
            "open_date": self.open_date,
            "account_type": self.account_type,
            "bank": self.bank.to_json(),
        }


class Transfer(models.Model):

    """
    Represents an account transfer to a branch.

    Attributes:
        account (Account): The account being transfered.
        branch (Branch): The branch to which the account is transferred.
    """

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return f"Account Transfered to {self.branch.name} Branch"

    def to_json(self):
        """Converts the Transfer instance to a JSON-like object."""
        return {
            "account": self.account.to_json(),
            "branch": self.branch.to_json(),
        }


class Withdraw(models.Model):

    """
    Represent a withdrawal from an account.

    Attributes:
        amount (float): The amount withdrawn.
        account (Account): The account from which the withdrawal is made.
    """

    amount = models.FloatField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)


class Deposit(models.Model):

    """
    Represent a deposit to an account.

    Attributes:
        amount (float): The amount deposited.
        account (Account): The account to which the deposit is made.
    """

    amount = models.FloatField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
