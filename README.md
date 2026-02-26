## Features
- Django + PostgreSQL
- Stripe Checkout (Test Mode)
- Quantity-based checkout
- Double charge protection (Stripe session id stored)
- Paid orders shown on same page (“My Orders”)

## How to Run
pip install -r requirements.txt  
python manage.py migrate  
python manage.py runserver  

## Stripe Test Card
4242 4242 4242 4242  
Any future date, any CVC

> Note: Stripe keys are test keys for assignment/demo purposes.
