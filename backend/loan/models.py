from django.db import models

from user.models import Customer


class EMI(models.Model):
    loan=models.ForeignKey('LoanApplication',on_delete=models.CASCADE)
    emi_date=models.DateField(unique=True)
    emi_amount=models.DecimalField(max_digits=10,decimal_places=2)
    paid=models.BooleanField(default=False)
    amount_paid=models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    amount_due=models.DecimalField(max_digits=10,decimal_places=2,default=0.00)

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
        return f"{self.user.name}'s {self.get_loan_type_display()} Loan Application"
