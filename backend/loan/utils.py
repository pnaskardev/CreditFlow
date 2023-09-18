from datetime import datetime, timedelta


def calculate_emi_due_dates(loan_amount, interest_rate, tenure, monthly_income, disbursement_date):
    # Constants
    DAYS_IN_MONTH = 30  # Assuming an average of 30 days in a month

    # Convert annual rate of interest to monthly rate
    monthly_rate = (int(interest_rate) / 100) / 12

    # Calculate the denominator part of the formula
    denominator = ((1 + monthly_rate) ** int(tenure)) - 1

    # Calculate EMI using the formula
    emi = (int(loan_amount) * monthly_rate *
           ((1 + monthly_rate) ** int(tenure))) / denominator

    # Calculate EMI due dates and amounts
    emi_schedule = []

    # Get the current date
    current_date = disbursement_date

    # Calculate the total amount payable
    # Rounded to 2 decimal places
    total_amount_payable = round(emi * int(tenure), 2)
    print(current_date)
    current_date=datetime.strptime(current_date,"%Y-%m-%dT%H:%M:%S.%fZ")
    for i in range(int(tenure)):
        # Calculate the first day of the next month
        first_day_of_next_month = (current_date+timedelta(days=32)).replace(
            day=1)

        # Calculate the EMI amount for the current month
        emi_schedule.append({
            'date': first_day_of_next_month.strftime("%Y-%m-%d"),
            # Rounded to 2 decimal places
            'amount_due': round(total_amount_payable - round(emi, 2),2)
        })
        total_amount_payable = total_amount_payable - round(emi, 2)
        if total_amount_payable<0.00:
            total_amount_payable=0
        # Move to the next month
        current_date = first_day_of_next_month

    return emi_schedule
