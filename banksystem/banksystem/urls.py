from django import views
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from . import views
from .views import CustomerDetailView, CustomerListView, CustomerAdd

urlpatterns = [
    path("base/", views.base, name="base"),
    path("customers/", CustomerListView.as_view(), name="customer_list"),
    path("<int:customer_id>/", CustomerDetailView.as_view(), name="customer-detail"),
    path("customer-add/", CustomerAdd.as_view(), name="customer_add"),
    path("branches/", views.branch_list, name="branch_list"),
    path("branch-add/", views.branch_add, name="branch_add"),
    path("admin/", admin.site.urls),
    url(r"^api-auth/", include("rest_framework.urls")),
    url(r"^api/", include("api.urls")),
    # path("branches/", BranchesAPIView.as_view(), name="branch-list"),
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
