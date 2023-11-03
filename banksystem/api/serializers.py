from rest_framework import serializers

from .models import *


class BranchSerializer(serializers.ModelSerializer):
    """
    Serializer for the Branch model.

    Attributes:
        id (int): Automatically generated unique identifier.
        name (str): The name of the branch.
        address (str): The address of the branch.
        branch_code (str): The branch code.
    """

    class Meta:
        model = Branch
        fields = "__all__"
        read_only_fields = ("id",)


class BranchDetailSerializer(serializers.ModelSerializer):

    """
    Detailed serializer for the Branch model. Includes all fields.

    Attributes:
        id (int): Automatically generated unique identifier.
        name (str): The name of the branch.
        address (str): The address of the branch.
        branch_code (str): The branch code.
    """

    class Meta:
        model = Branch
        fields = "__all__"


class BankSerializer(serializers.ModelSerializer):

    """
    Serializer for the Bank model.

    Attributes:
        id (int): Automatically generated unique identifier.
        name (str): The name of the bank.
        branch (Branch): The associated branch.
    """

    branch = BranchSerializer()

    class Meta:
        model = Bank
        fields = "__all__"
        read_only_fields = ("id",)


class ClientManagerSerializer(serializers.ModelSerializer):

    """
    Serializer for the ClientManager model.

    Attributes:
        id (int): Automatically generated unique identifier.
        name (str): The name of the client manager.
    """

    class Meta:
        model = ClientManager
        fields = "__all__"
        read_only_fields = ("id",)


class ClientSerializer(serializers.ModelSerializer):

    """
    Serializer for the Client model.

    Attributes:
        id (int): Automatically generated unique identifier.
        name (str): The name of the client.
        address (str): The address of the client.
    """

    class Meta:
        model = Client
        fields = "__all__"
        read_only_fields = ("id",)


class AccountSerializer(serializers.ModelSerializer):

    """
    Serializer for the Account model.

    Attributes:
        id (int): Automatically generated unique identifier.
        client (Client): The associated client.
        open_date (str): The date the account was opened.
        account_type (str): The type of the account.
        bank (Bank): The associated bank.
    """

    client = ClientSerializer()
    bank = BankSerializer()

    class Meta:
        model = Account

        fields = "__all__"
        read_only_fields = ("id",)


class AccountDetailSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    bank = BankSerializer()
    balance = serializers.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        model = Account
        fields = ["client", "bank", "balance", "open_date", "account_type"]


class TransferSerializer(serializers.ModelSerializer):

    """
    Serializer for the Transfer model.

    Attributes:
        id (int): Automatically generated unique identifier.
        account (Account): The associated account.
        branch (Branch): The branch to which the account is transferred.
    """

    class Meta:
        model = Transfer
        fields = "__all__"
        read_only_fields = ("id",)


class WithdrawSerializer(serializers.ModelSerializer):

    """
    Serializer for the Withdraw model.

    Attributes:
        id (int): Automatically generated unique identifier
        amount (float): The amount withdrawn.
        account (Account): The associated account from which the withdrawal is made.
    """

    class Meta:
        model = Withdraw
        fields = "__all__"
        read_only_fields = ("id",)


class DepositSerializer(serializers.ModelSerializer):
    """
    Serializer for the Deposit model.

    Attributes:
        id (int): Automatically generated unique identifier.
        amount (float): The amount deposited.
        account (Account): The associated account to which the deposit is made.
    """

    class Meta:
        model = Deposit
        fields = "__all__"
        read_only_fields = ("id",)
