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

    class Meta:
        verbose_name_plural = "Branches"

    def __str__(self):
        return self.name
