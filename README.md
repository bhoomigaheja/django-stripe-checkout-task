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
## Screenshots

### Products Page
<img width="1920" height="1818" alt="screencapture-127-0-0-1-8000-2026-02-26-16_30_43" src="https://github.com/user-attachments/assets/c99b03ce-7aa8-4edc-80e7-910db09e863e" />


### Stripe Checkout (Test Mode)
<img width="1920" height="912" alt="screencapture-checkout-stripe-c-pay-cs-test-a1FJnzjEU6FuT7EZYSDaXmGG6w2LHmIUR9QAl3huYdwxK5E8wyUClGqK1F-2026-02-26-16_31_09" src="https://github.com/user-attachments/assets/29194221-3d86-45ba-8147-099b4d91bb0a" />


### My Orders (After Payment)
<img width="1920" height="1962" alt="screencapture-127-0-0-1-8000-2026-02-26-16_31_30" src="https://github.com/user-attachments/assets/8cf6aaa5-da4c-4085-8df4-78b60c5d375c" />

