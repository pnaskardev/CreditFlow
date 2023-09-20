from django.db import models

from datetime import datetime, timedelta

from user.models import Customer
from .utils import calculate_total_amount_payable, calculate_emi


class EMI(models.Model):
    loan = models.ForeignKey(
        'LoanApplication', related_name='loan', on_delete=models.CASCADE)
    emi_date = models.DateField()
    amount_paid = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)

    def get_interest(self):
        return self.loan.interest_rate


# LoanApplication model
"""
Optimizations could have been done in the following model:
 - adding LoanTypes as a separate model and using a foreign key to it

LoanApplication model has the following properties:
    - user: Foreign Key to Customer model
    - loan_type: Type of loan
    - loan_amount: Amount of loan
    - interest_rate: Interest rate of loan
    - term_period: Term period of loan
    - disbursement_date: Date of disbursement of loan
"""
class LoanApplication(models.Model):

    LOAN_TYPES = (
        ('Car', 'Car Loan'),
        ('Home', 'Home Loan'),
        ('Education', 'Educational Loan'),
        ('Personal', 'Personal Loan'),
    )

    user = models.ForeignKey(
        Customer, related_name='user', on_delete=models.CASCADE)
    loan_type = models.CharField(choices=LOAN_TYPES, max_length=10)
    loan_amount = models.PositiveIntegerField()  # In rupees
    interest_rate = models.DecimalField(max_digits=10, decimal_places=2)
    term_period = models.IntegerField()  # In months
    disbursement_date = models.DateTimeField(auto_now_add=True)

    # Custom properties for the model
    @property
    def total_payable(self):
        return calculate_total_amount_payable(self.loan_amount, self.interest_rate, self.term_period)

    @property
    def amount_due(self):
        queryset = self.loan.all()
        # Extract 'amount_paid' values as a flat list
        amounts_paid = queryset.values_list('amount_paid', flat=True)
        total_amount_paid = sum(amounts_paid)  # Sum the extracted values

        return round(float(self.total_payable)-float(total_amount_paid), 2)

    @property
    def tenure_left(self):
        return self.term_period-len(self.loan.all())

    @property
    def emi_amount(self):
        return round(calculate_emi(self.interest_rate, self.principal_due, self.tenure_left), 2)

    @property
    def principal_due(self):
        queryset = self.loan.all()
        amounts_paid = queryset.values_list('amount_paid', flat=True)
        total_emi_paid = sum(amounts_paid)
        months_paid = len(queryset)
        monthly_interest = (self.interest_rate/100)/12
        total_interest_paid = months_paid*monthly_interest

        principal_due = self.loan_amount-(total_emi_paid-(total_interest_paid))

        return round(principal_due, 2)

    @property
    def interest_due(self):
        queryset = self.loan.all()
        months_paid = len(queryset)
        monthly_interest = (self.interest_rate/100)/12
        total_interest_paid = months_paid*monthly_interest

        interest_due = float(self.total_payable) - \
            float(self.loan_amount)-float(total_interest_paid)

        return round(interest_due, 2)

    def __str__(self):
        return f"{self.user.name}'s {self.get_loan_type_display()} Loan Application"
