import os
import csv

from celery import shared_task

from django.conf import settings

@shared_task
def calculate_credit_score(uuid):
    try:
        print(uuid)
        # print("Calculating credit score for user with uuid: {uuid}")

        csv_file_path=os.path.join(settings.BASE_DIR, 'transactions_data Backend.csv')

        if os.path.exists(csv_file_path):
            with open(csv_file_path, 'r') as csvfile:
                csv_reader=csv.DictReader(csvfile)
                for row in csv_reader:
                    if row['user']==uuid:
                        print(row['user'], row['date'],row['transaction_type'], row['amount'])
        else:
            print("File does not exist")
    except Exception as e:
        print(f"Error processing CSV file: {str(e)}")
