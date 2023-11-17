from django.contrib import admin
from .models import Customer


class CustomerAdmin(admin.ModelAdmin):
    exclude = ("balance", "username", "initial_balance")
    list_display = ("name", "address", "phone_number")

    def get_list_display(self, request):
        # Exclude 'balance' from the displayed fields
        return [
            field for field in super().get_list_display(request) if field != "balance"
        ]


admin.site.register(Customer, CustomerAdmin)
