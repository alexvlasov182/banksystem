from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, Branch
from .forms import BranchForm
from django.views import View


class CustomerListView(View):
    """
    View to list all customers.
    """

    template_name = "customer/customer_list.html"

    def get(self, request):
        customers = Customer.objects.all()
        context = {"customers": customers}
        return render(request, self.template_name, context)


class CustomerDetailView(View):
    """
    View to display the details of a customer.
    """

    template_name = "customer/customer_detail.html"

    def get(self, request, customer_id):
        customer = get_object_or_404(Customer, id=customer_id)
        context = {"customer": customer}
        return render(request, self.template_name, context)


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
