from datetime import datetime, timedelta
from rest_framework.response import Response

def calculate_emi_due_dates(loan_amount, interest_rate, tenure, monthly_income):
    # Constants
    DAYS_IN_MONTH = 30  # Assuming an average of 30 days in a month

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

    for _ in range(tenure):
        current_date += timedelta(days=DAYS_IN_MONTH)
        emi_due_dates.append(current_date)

    return emi_due_dates, emi
