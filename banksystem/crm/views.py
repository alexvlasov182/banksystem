from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone

from .forms import CreateUserForm, LoginForm


def homepage(request):
    """
    Render the homepage with the current date
    """
    current_date = timezone.now()
    return render(request, "crm/index.html", {"current_date": current_date})


def register(request):
    """
    Handle user registration.
    """
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect("my-login")
        else:
            messages.error(request, "Error in registration. Please check the form.")

    context = {"registerform": form}

    return render(request, "crm/register.html", context=context)


def my_login(request):
    """
    Handle user login.
    """
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid login credentials. Please try again")

    context = {"loginform": form}
    return render(request, "crm/my-login.html", context=context)


def user_logout(request):
    """
    Log out the user.
    """
    logout(request)
    return redirect("")


@login_required(login_url="my-login")
def dashboard(request):
    """
    Render the user dashboard.
    """
    return render(request, "crm/dashboard.html")
