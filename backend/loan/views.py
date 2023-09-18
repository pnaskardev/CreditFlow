from datetime import datetime, timedelta
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from . models import EMI, LoanApplication
from . serializers import LoanApplicationSerializer


class LoanApplicationCreateApiView(generics.CreateAPIView):
    serializer_class = LoanApplicationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Calculate EMI due dates

            
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            # Return an error response with validation errors
            response_data = {
                'Loan_id': None,
                'Due_dates': [],
                'Error': serializer.errors
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
