from django.contrib import admin
from .models import Branch, Bank

# Register your models here.

# Register the Branch model with the admin site.
admin.site.register(Branch)
# Register the Bank model with the admin site.
admin.site.register(Bank)
