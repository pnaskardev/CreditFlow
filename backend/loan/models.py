from django.db import models

from user.models import Customer


class EMI(models.Model):
    loan=models.ForeignKey('LoanApplication',on_delete=models.CASCADE)
    emi_date=models.DateTimeField()
    emi_amount=models.DecimalField(max_digits=10,decimal_places=2)

class LoanTypeLimit(models.Model):
    LOAN_TYPES = (
        ('Car', 'Car Loan'),
        ('Home', 'Home Loan'),
        ('Education', 'Educational Loan'),
        ('Personal', 'Personal Loan'),
    )

    loan_type = models.CharField(
        max_length=20, choices=LOAN_TYPES, unique=True)
    max_loan_amount = models.DecimalField(
        max_digits=10, decimal_places=2)  # In rupees

    def __str__(self):
        return self.loan_type


# LoanApplication model
class LoanApplication(models.Model):

    LOAN_TYPES = (
        ('Car', 'Car Loan'),
        ('Home', 'Home Loan'),
        ('Education', 'Educational Loan'),
        ('Personal', 'Personal Loan'),
    )

    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # loan_type = models.ForeignKey('LoanTypeLimit', on_delete=models.CASCADE)
    loan_type = models.CharField(choices=LOAN_TYPES, max_length=10)
    loan_amount = models.DecimalField(
        max_digits=10, decimal_places=2)  # In rupees
    interest_rate=models.DecimalField(max_digits=10,decimal_places=2)
    term_period=models.IntegerField() # In months
    disbursement_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s {self.get_loan_type_display()} Loan Application"

    # def clean(self):
    #     # Check credit score, annual income, and loan amount conditions
    #     if self.user.credit_score < 450:
    #         raise ValidationError(
    #             "Credit score must be >= 450 to apply for a loan.")

    #     if self.user.annual_income < 150000:
    #         raise ValidationError(
    #             "Annual income must be >= Rs. 1,50,000 to apply for a loan.")

    #     if self.loan_type == 'Car' and self.loan_amount > 750000:
    #         raise ValidationError(
    #             "Car loan amount cannot exceed Rs. 7,50,000.")
    #     elif self.loan_type == 'Home' and self.loan_amount > 8500000:
    #         raise ValidationError(
    #             "Home loan amount cannot exceed Rs. 85,00,000.")
    #     elif self.loan_type == 'Education' and self.loan_amount > 5000000:
    #         raise ValidationError(
    #             "Educational loan amount cannot exceed Rs. 50,00,000.")
    #     elif self.loan_type == 'Personal' and self.loan_amount > 1000000:
    #         raise ValidationError(
    #             "Personal loan amount cannot exceed Rs. 10,00,000.")
