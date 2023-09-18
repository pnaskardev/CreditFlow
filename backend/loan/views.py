from datetime import datetime, timedelta
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from user.models import Customer
from . models import EMI, LoanApplication
from . serializers import LoanApplicationSerializer
from . utils import calculate_emi_due_dates

class LoanApplicationCreateApiView(generics.CreateAPIView):
    serializer_class = LoanApplicationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():

            serializer.save()
            # Calculate EMI due dates
            emi_due_dates = []
            loan_id = serializer.data.get('id')
            disbursement_date = serializer.data.get('disbursement_date')
            # disbursement_date = datetime.strptime(disbursement_date,'%Y-%m-%d')

            id = serializer.data.get('user')
            loan_applicant=Customer.objects.get(adhaar_id=id)
            annual_income=loan_applicant.annual_income
            # Calculate EMI due dates starting from the following month
            res=calculate_emi_due_dates(
                loan_amount=float(serializer.data.get('loan_amount')),
                interest_rate=float(serializer.data.get('interest_rate')),
                tenure=int(serializer.data.get('term_period')),
                monthly_income=int(annual_income)/12,
                disbursement_date=disbursement_date
            )


            return Response({"loan_id":loan_id,"loan_due_dates":res}, status=status.HTTP_201_CREATED)
        else:
            # Return an error response with validation errors
            response_data = {
                'Loan_id': None,
                'Due_dates': [],
                'Error': serializer.errors
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
