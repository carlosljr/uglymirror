# uglymirror
A security CRUD web application with an ugly frontend.

# General

- WEB app developed with Django framework
- PostgreSQL database authenticated transactions
- Encryption mechanisms for security:
    - django-sha2: strong password hashing app, using a combination of Bcrypt and HMAC with multiple secret keys.
    - django-fernet-fields: Symmetric encryption app to hide confidential data in DB.
- Signup feature with confirmation mail
- Password reset procedure
- Protection against XSS (Cross site scripting) attacks
- CSRF (Cross Site Request Forgery) protection
- Clickjacking bullet proof with Django Middleware
- Requests redirects to HTTPS only
- Usage of secure cookie sessions
- HSTS header for HTTPS future connections

# Usage instructions

Step 1

The following dependencies are required before running the app:

  - django-sha2
  - python-decouple
  - psycopg2
  - django-fernet-fields

For heroku deploy, the following dependencies are required as well:

  - gunicorn
  - whitenoise
  - dj-database-url

All dependencies are available in PyPI and can be installed with pip install command.

Step 2

Create a .env file with environment variables values set in settings.py. All variables with config attribute in this file needs a value configured in an .env file.

In this step, you need to configure DB username and password used in your local Postgres to manipulate the schema and create, select, delete actions.

Step 3

For tests proposal, use django.core.mail.backends.console.EmailBackend instead of email configurations.

With you don't have any domain with a SMTP server configured to sent mails, you can try to use your personal email with SMTP email provider. But, it is not RECOMMENDED to do that!

Step 4

Run the app with the following sequence:

  - 1 - python manage.py createsuperuser --> Create a default superuser to test 
  - 2- python manage.py makemigrations --> To create the migrations in uglymirror model
  - 3- python manage.py migrate --> To create tables with entries defined in models
  -4- python manage.py runserver --> To run the app on localhost, port 8000

Good luck and be safe! :)


