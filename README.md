# CreditFlow

The Loan Management System is a Django-based application designed to help a Loan service company efficiently lend loans to users. The system provides functionalities to register users, calculate their credit scores, apply for loans, manage loan details, calculate EMIs, and track payments. This project adheres to best practices in Django development, including models, views, APIs, flows, and authentication.


## Table of Contents

- [Run Locally](#Run-Locally)
- [APIs](#apis)
- [Contributing](#contributing)
- [Contact](#contact)



## Tech Stack

- **Server:** Django, Django REST Framework
- **Database:** PostgreSQL
- **Message Queue:** Celery
- **Message Broker:** Redis
- **Deployment:** Docker Compose

## Run Locally

Clone the project

```bash
  git clone https://github.com/pnaskardev/CreditFlow
```

Go to the project directory

```bash
  cd CreditFlow
```

Start backend on docker

```bash
docker-compose -d --build

```




## API Reference

**Please note that all of these routes can be accessed through Django Rest Framework HTML Forms for easy access.**

- **Register User:** `POST http://127.0.0.1:8001/api/register-user/`.

  - **Done automatically through sampple data**


- **Loan Application Create View** `POST http://127.0.0.1:8001/api/apply-loan/`
  Apply for a loan.

- | field |              |
  | :-------- | :------------------------- |
  | `unique_user_id:`  | Required |
  | `loan_type:`  | Required |
  | `loan_amount`  | Required |
  | `interest_rate`  | Required |
  | `term_period`  | Required |
  | `disbursement_date`  | Required |

- **Make Payment:** `PATCH http://127.0.0.1:8001/api/make-payment/<int:loan_id>/`
 Make Payment for a loan with loan_id.

- | field |              |
  | :-------- | :------------------------- |
  | `Loan_id:`  | Required |
  | `amount`  | Required |

- **Get Loan Statement** `http://127.0.0.1:8001/api/get-statement/<int:loan_id>/`
  Get Loan Statement with loan_id
- | field |              |
  | :-------- | :------------------------- |
  | `Loan_id:`  | Required |
## Authors

- [@pnaskardev](https://www.github.com/pnaskardev)

