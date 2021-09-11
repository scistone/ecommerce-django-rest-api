# DRF Ecommerce
Open Source E-commerce API System with Django Rest Framework. The development process still continues.

# Get Started

## Installation

Use the git clone to install drf-ecommerce.

```bash
git clone https://github.com/scistone/drf-ecommerce.git
```

### Installation of required packages 
```bash
cd drf-ecommerce
pip install -r requirements.txt
```

### Creating the database

```bash
cd ecommerce
python manage.py makemigrations
python manage.py migrate
```

### Run

```
python manage.py runserver
```

## Configuration

### Mail Configuration

We used SendGrid for the mail system. [SendGrid Django Documantation](https://docs.sendgrid.com/for-developers/sending-email/django)

```python
### EMAIL SETTINGS FOR SENDGRID
from dotenv import load_dotenv
import os

load_dotenv()

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey' # this is exactly the value 'apikey'
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = FROM_EMAIL
```
In order to use:
1. Create '.env' file in root folder
2. Create variables SENDGRID_API_KEY and DEFAULT_FROM_EMAIL
3. and ready to use!

API endpoints
=============
Auth
-----
- api/auth/register/ (POST)
    - first_name
    - last_name
    - email
    - password

    Returns User object and Token key

- api/auth/login/ (POST)

    - email
    - password

    Returns User object and Token key

- api/auth/logout/ (POST)

- api/auth/logoutall/ (POST)

- api/auth/user/ (GET)

    - id
    - first_name
    - last_name
    - email

- api/auth/change_password/ (POST)
    
    - old_password
    - password
    - password2

- api/auth/user/update/ (POST)
    
    - first_name
    - last_name

- api/auth/request-reset-email/ (POST)

    - email

- api/auth/password-reset/uidb64/token/ (GET)

    This api check the uidb64 and token. 

- api/auth/password-reset-complete/ (POST)

    - password
    - token
    - uidb64
