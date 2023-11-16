from django import views
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from . import views
from django.urls import path
from .views import SignUpView, CustomLoginView, CustomLogoutView, customer_dashboard


urlpatterns = [
    path("", views.homepage, name=""),
    path("signup", SignUpView.as_view(), name="signup"),
    path("login", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("dashboard/", customer_dashboard, name="customer_dashboard"),
    path("admin/", admin.site.urls),
    url(r"^api-auth/", include("rest_framework.urls")),
    url(r"^api/", include("api.urls")),
    # path("branches/", BranchesAPIView.as_view(), name="branch-list"),
    path("", include("crm.urls")),
]

"""
banksystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information, please see:
https://docs.djangoproject.com/en/3.2/topics/http/urls/

Examples:
Function views:
1. Add an import: from my_app import views
2. Add a URL to urlpatterns: path('', views.home, name='home')

Class-based views:
1. Add an import: from other_app.views import Home
2. Add a URL to urlpatterns: path('', Home.as_view(), name='home')

Including another URLconf:
1. Import the include() function: from django.urls import include, path
2. Add a URL to urlpatterns: path('blog/', include('blog.urls'))
"""
