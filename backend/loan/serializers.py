from rest_framework import serializers
from django.shortcuts import get_object_or_404

from . utils import calculate_emi, calculate_monthly_income, calculate_interest_earned
from loan.models import LoanApplication, EMI


class LoanApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoanApplication
        fields = '__all__'

    def validate(self, attrs):

        # Get the information Attributes
        loan_type = attrs.get('loan_type')
        annual_income = attrs.get('user').annual_income
        loan_amount = attrs.get('loan_amount')
        interest_rate = attrs.get('interest_rate')
        tenure = attrs.get('term_period')

        credit_score = None
        try:
            # credit_score = get_object_or_404(attrs.get('user').credit_score)
            credit_score = attrs.get('user').credit_score
        except:
            raise serializers.ValidationError(
                "Credit score not found. Loan Cannot be disbursed.")

        credit_score = credit_score.get_credit_score()

        # Check credit score
        if int(credit_score) < 450:
            raise serializers.ValidationError(
                "Credit score must be >= 450 to apply for a loan.")
        # Check interest rate
        if int(interest_rate) < 14:
            raise serializers.ValidationError("Interest rate should be >= 14%")
        # Check annual income
        if int(annual_income) < 150000:
            raise serializers.ValidationError(
                "Annual income must be >= Rs. 1,50,000 to apply for a loan.")

        # Check loan amount bounds based on loan type
        if loan_type == 'Car' and int(loan_amount) > 750000:
            raise serializers.ValidationError(
                "Car loan amount cannot exceed Rs. 7,50,000.")

        elif loan_type == 'Home' and int(loan_amount) > 8500000:
            raise serializers.ValidationError(
                "Home loan amount cannot exceed Rs. 85,00,000.")
        elif loan_type == 'Education' and int(loan_amount) > 5000000:
            raise serializers.ValidationError(
                "Educational loan amount cannot exceed Rs. 50,00,000.")
        elif loan_type == 'Personal' and int(loan_amount) > 1000000:
            raise serializers.ValidationError(
                "Personal loan amount cannot exceed Rs. 10,00,000.")

        # Calculate Monthly Income of the Loan Applicant
        monthly_income = calculate_monthly_income(annual_income=annual_income)

        # Calculate Monthly EMI of the applied loan
        emi = calculate_emi(interest_rate=interest_rate,
                            loan_amount=loan_amount, tenure=tenure)
        max_allowed_emi = 0.60 * monthly_income

        # If the sanctioned EMI is more than the 60% of monthly income
        # reject the loan application
        if emi > max_allowed_emi:
            raise serializers.ValidationError(
                "EMI cannot exceed 60% of monthly income.")

        total_interest_earned = calculate_interest_earned(
            loan_amount=loan_amount, emi=emi, tenure=tenure)
        if total_interest_earned < 10000:
            raise serializers.ValidationError(
                "Interest earned should be greater than 10000")

        return attrs


class PayEMISerializer(serializers.ModelSerializer):

    class Meta:
        model = EMI
        fields = ['loan_id', 'emi_amount']


class UpcomingEMISerializer(serializers.ModelSerializer):

    class Meta:
        model = EMI
        fields = ['emi_date', 'amount_due']


class RetrieveEMISerializer(serializers.ModelSerializer):
    principal_amount = serializers.SerializerMethodField()
    interest_amount = serializers.SerializerMethodField()

    class Meta:
        model = EMI
        fields = ['emi_date', 'emi_amount',
                  'amount_due', 'principal_amount', 'interest_amount']

    def get_principal_amount(self, obj):
        print(obj)
        interest_rate = obj.loan.interest_rate
        monthly_interest_rate = (int(interest_rate) / 100) / 12
        # print(monthly_interest_rate)
        interest_component = round(
            float(obj.loan.loan_amount) * monthly_interest_rate, 2)
        principal_component = round(
            float(obj.emi_amount) - interest_component, 2)
        return principal_component

    def get_interest_amount(self, obj):
        principal_component = self.get_principal_amount(obj)
        interest_component = float(obj.emi_amount)-principal_component
        return interest_component
