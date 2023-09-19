from datetime import datetime, timedelta


def calculate_monthly_income(annual_income):
    monthly_income = int(annual_income)//12
    return monthly_income


def calculate_emi(interest_rate, loan_amount, tenure):
    # Convert annual rate of interest to monthly rate
    monthly_rate = (int(interest_rate) / 100) / 12

    # Calculate the denominator part of the formula
    denominator = ((1 + monthly_rate) ** int(tenure)) - 1

    # Calculate EMI using the formula
    emi = (int(loan_amount) * monthly_rate *
           ((1 + monthly_rate) ** int(tenure))) / denominator

    return emi


def calculate_emi_due_dates(loan_amount, interest_rate, tenure, annual_income, disbursement_date):

    sanctioned_emi = calculate_emi(
        interest_rate=interest_rate, loan_amount=loan_amount, tenure=tenure)

    # Calculate EMI due dates and amounts
    emi_schedule = []

    # Get the current date
    current_date = disbursement_date

    # Calculate the total amount payable
    # Rounded to 2 decimal places
    total_amount_payable = round(sanctioned_emi * int(tenure), 2)

    current_date = datetime.strptime(current_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    for i in range(int(tenure)):
        # Calculate the first day of the next month
        first_day_of_next_month = (current_date+timedelta(days=32)).replace(
            day=1)

        total_amount_payable = round(
            total_amount_payable - round(sanctioned_emi, 2), 2)
        if total_amount_payable < 0.00:
            total_amount_payable = 0.00

        if total_amount_payable < sanctioned_emi:
            sanctioned_emi = total_amount_payable

        # Calculate the EMI amount for the current month
        emi_schedule.append({
            'date': first_day_of_next_month.strftime("%Y-%m-%d"),
            # Rounded to 2 decimal places
            'amount_due': total_amount_payable,
            'emi_amount': round(sanctioned_emi, 2),
        })

        # Move to the next month
        current_date = first_day_of_next_month

    return emi_schedule
