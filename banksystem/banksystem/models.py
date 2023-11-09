from django.db import models
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)


class Customer(models.Model):
    """
    Represent a customer in the application.

    Attributes:
        first_name (str): The first name of the customer.
        last_name (str): The last name of the customer.
        email (str): The email address of the customer.
        age (int): The date of birth of the customer.
        created_at (datetime): The timestamp when the customer record was created.
    """

    first_name = models.CharField(max_length=50, db_index=True)
    last_name = models.CharField(max_length=50, db_index=True)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Customers"

    def full_name(self):
        """
        Returns the full name of the customer.

        Returns:
            str: The full name in the format "First Last".
        """
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        """
        Return the string representation of the customer.
        """
        return self.full_name()

    def clean(self):
        """
        Validate the customer's age ot ensure they are 18 or older
        """
        if self.age < 18:
            raise ValidationError("Age must be 18 or older")

    def save(self, *args, **kwargs):
        """
        Save the customer recored, performing validation before saving.
        """
        try:
            self.full_clean()
            super(Customer, self).save(*args, **kwargs)
        except ValidationError as e:
            logger.error(f"Validation error when saving a Customer: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred when saving a Customer: {e}")


class Branch(models.Model):

    """
    Represent a bank branch

    Attributes:
        branch_name (str): The name of the branch.
        address (str): The address of the branch.
        branch_code (str): The branch code.

    Meta:
        verbose_name_plural = "Branches"

    Methods:
        __str__(): Returns the branch name a string.
    """

    branch_name = models.CharField(
        max_length=250, verbose_name="Branch Name", db_index=True
    )
    address = models.CharField(max_length=250, verbose_name="Address")
    branch_code = models.CharField(
        max_length=250, verbose_name="Branch Code", unique=True
    )

    class Meta:
        verbose_name_plural = "Branches"

    def __str__(self):
        """
        Returns the branch name as a string.
        """
        return self.name


class Bank(models.Model):
    """
    Represent a bank.

    Attributes:
        bank_name (str): The name of the bank. Must be unique
        bank_branch (Branch): The branch to which the bank belongs. Can be empty
    """

    bank_name = models.CharField(
        max_length=250, verbose_name="Bank Name", db_index=True, unique=True
    )
    bank_branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="banks",
        verbose_name="Bank Branch",
    )

    def __str__(self):
        "Returns the bank name as a string"
        return self.name
