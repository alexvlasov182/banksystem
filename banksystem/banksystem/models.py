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

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
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
        return self.full_name()

    def clean(self):
        """
        Validate the customer's age ot ensure they are 18 or older
        """
        if self.age < 18:
            raise ValidationError("Age must be 18 or older")

    def save(self, *args, **kwargs):
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
        name (str): The name of the branch.
        address (str): The address of the branch.
        branch_code (str): The branch code.

    Meta:
        verbose_name_plural = "Branches"
    """

    name = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    branch_code = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "Branches"

    def __str__(self):
        return self.name
