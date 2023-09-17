from . models import CreditScore, Customer
import os
import csv
import logging
from celery import shared_task
from django.conf import settings
from django.db import transaction


logger = logging.getLogger(__name__)


@shared_task
def calculate_credit_score(uuid):
    try:
        with transaction.atomic():
        # print(uuid)
        # print("Calculating credit score for user with uuid: {uuid}")

            csv_file_path = os.path.join(
                settings.BASE_DIR, 'transactions_data Backend.csv')

            credit_sum = 0
            debit_sum = 0

            if os.path.exists(csv_file_path):
                with open(csv_file_path, 'r') as csvfile:
                    csv_reader = csv.DictReader(csvfile)
                    for row in csv_reader:
                        if row['user'] == uuid:
                            print(row['user'], row['date'],row['transaction_type'], row['amount'])
                            if row['transaction_type'] == 'credit':
                                credit_sum += int(row['amount'])
                            else:
                                debit_sum += int(row['amount'])
                print(credit_sum, debit_sum)
                account_balance = credit_sum-debit_sum
                # Define the minimum and maximum credit score values
                min_credit_score = 300
                max_credit_score = 900

                credit_score = min_credit_score

                # Define the account balance thresholds
                lower_threshold = 100000  # Rs. 1,00,000
                upper_threshold = 1000000  # Rs. 10,00,000

                # Check if account_balance is less than or equal to the lower threshold
                if account_balance <= lower_threshold:
                    credit_score = min_credit_score

                # Check if account_balance is greater than or equal to the upper threshold
                if account_balance >= upper_threshold:
                    credit_score = max_credit_score

                if credit_score > min_credit_score and credit_score < max_credit_score:
                    # Calculate the credit score based on the intermediate balance
                    balance_difference = account_balance - lower_threshold
                    score_increment = balance_difference // 15000  # Rs. 15,000 increments
                    credit_score = min_credit_score + (score_increment * 10)

                current_customer = Customer.objects.get(adhaar_id=uuid)
                credit_score_instance = CreditScore.objects.create(
                    adhaar_id=current_customer, credit_score=credit_score)
                
                credit_score_instance.save()

                # transaction.commit()
                logger.info(
                    f"Credit score calculated for UUID {uuid}: {credit_score}")
                return credit_score
            else:
                print("File does not exist")
                return None
    except Exception as e:
        # print(f"Error processing CSV file: {str(e)}")
        logger.error(f"Error processing CSV file for UUID {uuid}: {str(e)}")
        return None  # or return an error code or message
