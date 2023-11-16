from django import template
from django.urls import reverse

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


register = template.Library()


@register.filter
def get_show_balance_url(account_number):
    return reverse("show_balance", kwargs={"account_number": account_number})
