from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Branch
from .forms import BranchForm


# from .forms import RegistrationForm


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
