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

            interest_rate = serializer.validated_data['interest_rate']
            loan_amount = serializer.validated_data['loan_amount']
            tenure = serializer.validated_data['term_period']
            monthly_income = serializer.validated_data['user'].annual_income
            
            # Constants
            DAYS_IN_MONTH = 30  # Assuming an average of 30 days in a month

            # Check if interest rate is >= 14%
            if interest_rate < 14:
                return Response({'message':'Interest rate should be >= 14%.'})

            # Calculate monthly interest rate
            monthly_interest_rate = (interest_rate / 100) / 12

            # Calculate EMI using the standard EMI calculation formula
            emi = loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** tenure
            emi /= ((1 + monthly_interest_rate) ** tenure) - 1

            # Check if total interest earned is > 10000
            total_interest = (emi * tenure) - loan_amount
            if total_interest <= 10000:
                return Response({'message':'Total interest earned should be > Rs. 10,000.'})

            # Check if EMI amount is at most 60% of monthly income
            if emi > (0.60 * (monthly_income / DAYS_IN_MONTH)):
                return Response({'message':'EMI amount should be at most 60%\ of monthly income.'})

            # Calculate EMI due dates starting from the following month
            emi_due_dates = []
            # Get the current date
            current_date = datetime.now()

            # Calculate the first day of the next month
            first_day_of_next_month = current_date.replace(day=1, month=current_date.month + 1)

            # If the current month is December, increment the year as well
            if current_date.month == 12:
                first_day_of_next_month = first_day_of_next_month.replace(year=current_date.year + 1, month=1)


            # Return the success response with loan ID and EMI due dates
            response_data = {
                'Loan_id': loan_application.id,
                'Due_dates': emi_records,
                'Error': None  # No error
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            # Return an error response with validation errors
            response_data = {
                'Loan_id': None,
                'Due_dates': [],
                'Error': serializer.errors
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
