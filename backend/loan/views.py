from datetime import datetime, timedelta
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from user.models import Customer
from . models import EMI, LoanApplication
from . serializers import LoanApplicationSerializer, PayEMISerializer, ListEmiSerializer, UpcomingEMISerializer


# API View to create a new Loan Application
class LoanApplicationCreateApiView(generics.CreateAPIView):
    serializer_class = LoanApplicationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            loan_application_instance = serializer.save()

            # Calculate EMI due dates
            loan_id = loan_application_instance.id

            loan_due_dates = []
            current_date = loan_application_instance.disbursement_date
            for i in range(int(loan_application_instance.term_period)):
                amount_due = loan_application_instance.emi_amount

                # Calculate the first day of the next month
                first_day_of_next_month = (current_date+timedelta(days=32)).replace(
                    day=1)

                formatted_date = first_day_of_next_month.strftime("%Y-%m-%d")

                loan_due_dates.append(
                    {"date": formatted_date, "amount_due": amount_due})
                current_date = first_day_of_next_month

            return Response({"loan_id": loan_id, "loan_due_dates": loan_due_dates}, status=status.HTTP_200_OK)
        else:
            # Return an error response with validation errors
            response_data = {
                'Loan_id': None,
                'Due_dates': [],
                'Error': serializer.errors
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

# API to pay EMI


class PayEMIApiView(generics.CreateAPIView):
    serializer_class = PayEMISerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_200_OK)


# API to retrieve the list of upcoming EMIs and Past transactions
class EMIRetrieveApiView(generics.ListAPIView):
    serializer_class = ListEmiSerializer

    def list(self, request, *args, **kwargs):

        loan_id = self.kwargs['loan_id']

        # IF loan exists then return the list of EMIs
        # else return an error message
        loan = get_object_or_404(LoanApplication, id=loan_id)

        # Get past paid EMI list
        past_emi_list = EMI.objects.filter(loan_id=loan_id)
        past_dues = self.get_serializer(past_emi_list, many=True)

        # Create the list of upcoming dues
        upcoming_dues = []
        tenure_left = loan.tenure_left

        last_emi_paid = EMI.objects.filter(loan_id=loan_id).last().emi_date
        current_date = last_emi_paid

        for i in range(tenure_left):
            next_emi_date = (current_date+timedelta(days=32)).replace(day=1)
            emi_amount = loan.emi_amount
            upcoming_dues.append(
                {"date": next_emi_date, "amount_due": round(emi_amount, 2)})
            current_date = next_emi_date

        return Response({"past_transactions": past_dues.data, "upcoming_emi_list": upcoming_dues}, status=status.HTTP_200_OK)
