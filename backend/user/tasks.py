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
        csv_file_path = os.path.join(
            settings.BASE_DIR, 'transactions_data Backend.csv')
        
        max_credit_score = 900
        min_credit_score = 300

        max_account_balance = 1000000
        min_account_balance = 100000

        if os.path.exists(csv_file_path):
            with open("transactions_data Backend.csv", 'r') as csvfile:
                csvreader = csv.reader(csvfile)

                for row in csvreader:
                    if row[0]==uuid:
                        if row[2]=="CREDIT":
                            credit_sum = credit_sum + int(row[3])
                        elif row[2]=="DEBIT":
                            debit_sum = debit_sum + int(row[3])
                        value=abs(credit_sum-debit_sum)
                        if value >=max_account_balance:
                            credit_score=max_credit_score
                        elif value<=min_account_balance:
                            credit_score=min_credit_score
                        else:
                            score_increment=value//15000
                            credit_score=score_increment*10+min_credit_score
                        print(value, credit_score)
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
