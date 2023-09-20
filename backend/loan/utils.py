# calculate_interest_earned function
def calculate_interest_earned(loan_amount, emi, tenure):
    loan_amount = int(loan_amount)
    emi = float(emi)
    tenure = int(tenure)
    total_amount = round(emi*tenure, 2)
    interest_earned = round(total_amount - loan_amount, 2)
    return interest_earned

# calculate_monthly_income function
def calculate_monthly_income(annual_income):
    monthly_income = int(annual_income)//12
    return monthly_income

# calculate_emi function
def calculate_emi(interest_rate, loan_amount, tenure):
    # Convert annual rate of interest to monthly rate
    monthly_rate = (int(interest_rate) / 100) / 12

    # Calculate the denominator part of the formula
    denominator = ((1 + monthly_rate) ** int(tenure)) - 1

    # Calculate EMI using the formula
    emi = (int(loan_amount) * monthly_rate *
           ((1 + monthly_rate) ** int(tenure))) / denominator

    return emi

def calculate_total_amount_payable(loan_amount, interest_rate, tenure):

    emi=calculate_emi(loan_amount=loan_amount,interest_rate=interest_rate,tenure=tenure)
    total_amount_payable=emi*tenure
    return total_amount_payable