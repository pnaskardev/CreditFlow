from rest_framework import serializers
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta


from . utils import calculate_emi, calculate_monthly_income, calculate_interest_earned
from loan.models import LoanApplication, EMI


class LoanApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoanApplication
        fields = ['user', 'loan_type', 'loan_amount', 'interest_rate', 'term_period', 'disbursement_date',
                  'total_payable', 'amount_due']

    # All the loan related validation has been done here in the serializer
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

        # total intereset earned should be greater than
        total_interest_earned = calculate_interest_earned(
            loan_amount=loan_amount, emi=emi, tenure=tenure)
        if total_interest_earned < 10000:
            raise serializers.ValidationError(
                "Interest earned should be greater than 10000")

        return attrs


class PayEMISerializer(serializers.ModelSerializer):

    class Meta:
        model = EMI
        fields = ['loan', 'amount_paid']

    def validate(self, attrs):
        loan_id = attrs.get('loan')
        current_date = datetime.now().date()
        next_emi_date = (current_date + timedelta(days=32)).replace(day=1)
        # check if already paid
        if len(EMI.objects.filter(loan_id=loan_id, emi_date=next_emi_date)) != 0:
            raise serializers.ValidationError(
                "EMI for this date is already paid")
        attrs['emi_date'] = next_emi_date
        return super().validate(attrs)

    def create(self, validated_data):
        return super().create(validated_data)


class UpcomingEMISerializer(serializers.ModelSerializer):

    class Meta:
        model = LoanApplication
        fields = ['emi_date', 'amount_due']


class ListEmiSerializer(serializers.ModelSerializer):
    principal_due = serializers.SerializerMethodField()
    interest_due = serializers.SerializerMethodField()
    amount_due = serializers.SerializerMethodField()

    class Meta:
        model = EMI
        fields = ['emi_date', 'amount_paid',
                  'amount_due', 'principal_due', 'interest_due']

    def get_amount_due(self, obj):
        return obj.loan.amount_due

    def get_principal_due(self, obj):
        return obj.loan.principal_due

    def get_interest_due(self, obj):
        return obj.loan.interest_due
