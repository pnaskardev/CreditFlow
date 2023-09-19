from rest_framework import serializers

from . utils import calculate_emi, calculate_monthly_income
from loan.models import LoanApplication, EMI


class LoanApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoanApplication
        fields = '__all__'

    def validate(self, attrs):

        # Get the information Attributes
        loan_type = attrs.get('loan_type')
        credit_score = attrs.get('user').credit_score
        annual_income = attrs.get('user').annual_income
        loan_amount = attrs.get('loan_amount')
        interest_rate = attrs.get('interest_rate')
        tenure = attrs.get('term_period')
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
        return attrs


class PayEMISerializer(serializers.ModelSerializer):

    class Meta:
        model = EMI
        fields = ['loan_id', 'emi_amount']


class RetrieveEMISerializer(serializers.ModelSerializer):

    class Meta:
        model = EMI
        fields = '__all__'
