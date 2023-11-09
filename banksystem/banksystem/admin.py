from django.contrib import admin
from .models import Branch, Customer, Bank

# Register your models here.

# Register the Branch model with the admin site.
admin.site.register(Branch)
# Register the Customer model with the admin site.
admin.site.register(Customer)
# Register the Bank model with the admin site
admin.site.register(Bank)
