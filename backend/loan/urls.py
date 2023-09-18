from django.urls import path, include

from . views import LoanApplicationCreateApiView

urlpatterns = [
    path('api/apply-loan/', LoanApplicationCreateApiView.as_view(), name='Customer'),
]
