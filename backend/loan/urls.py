from django.urls import path, include

from . views import LoanApplicationCreateApiView, EMIRetrieveApiView, PayEMIApiView

urlpatterns = [
    path('api/apply-loan/', LoanApplicationCreateApiView.as_view(), name='apply-loan'),
    path('api/make-payment/', PayEMIApiView.as_view(), name='make-payment'),
    path('api/get-statement/<int:loan_id>/', EMIRetrieveApiView.as_view(), name='get-statement'),
]
