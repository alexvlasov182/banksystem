from django.conf.urls import url

from .views import (
    BranchesAPIView,
)

urlpatterns = [
    url(r"^branches/$", BranchesAPIView.as_view(), name="branches"),
]
