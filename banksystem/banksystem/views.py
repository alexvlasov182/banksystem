from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Customer, Branch
from .forms import BranchForm, CustomerForm


class CustomerListView(View):
    """
    View to list all customers.
    """

    template_name = "customer/customer_list.html"

    def get(self, request):
        """
        Handle GET request to list all customers.

        Args:
            request: The HTTP request object.

        Returns:
            A response with a list of customers.
        """
        customers = Customer.objects.all()
        context = {"customers": customers}
        return render(request, self.template_name, context)


class CustomerDetailView(View):
    """
    View to display the details of a customer.
    """

    template_name = "customer/customer_detail.html"

    def get(self, request, customer_id):
        """
        Handle GET request to display the details of a customer.

        Args:
            request: The HTTP request object.
            customer_id: The ID of the customer to disply.

        Returns:
            A response with customer details.
        """
        customer = get_object_or_404(Customer, id=customer_id)
        context = {"customer": customer}
        return render(request, self.template_name, context)


class CustomerAdd(View):
    """
    Add customer to database
    """

    template_name = "customer/customer_add.html"

    def get(self, request):
        """
        Handle GET request to show the customer addition form.

        Args:
            request: The HTTP request object.

        Returns:
            A response with the customer addition form.
        """
        form = CustomerForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("customer_list")
        return render(request, self.template_name, {"form": form})


def base(request):
    return render(request, "base.html")


def branch_list(request):
    branches = Branch.objects.all()
    return render(request, "branch_list.html", {"branches": branches})


def branch_add(request):
    if request.method == "POST":
        form = BranchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("branch_list")

    else:
        form = BranchForm()
    return render(request, "branch_add.html", {"form": form})
