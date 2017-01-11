# django-SurveysManager
This project contains the necessary code for implementing a new survey manager application.

## Installation

In order to make this project work, it's necessary to build a virtual environment with a version of Python 2.7.

Afterwards, you just have to load the virtualenv and type the command below:

`pip install -r requirements.txt`

Then, you will need a user-admin so you have to run the command:

`python manage.py createsuperuser`

(Signup is based on the email address so I recommend setting up the username with the same email address too)

Then, run the server with the next command:

`python manage.py runserver`

Finally, the superuser is not created with a user-extended profile, so you should create a basic user-profile
for him manually. To do that, just go to **127.0.0.1/admin** and **create manually the user-profile** record matching with
the superuser.

**Additional Information:**

When users are registered in the web site, their active field is set up to False (because we are waiting for receiving
an activation email) so that the superuser should activate manually to make them work.

## Features

* Theme:
  - Start Bootstrap freelancer
  
* Front-end Libraries & Frameworks:
  - Bootstrap
  - Bootstrap-datepicker
  - Bootstrap-toggle
  - Fileinput
  - jquery.js

* Database:
  - sqLite3 (If you want to change it, you just need to set up the new one and make a migration)
  

## Contributors

If you want to know more about me, just visit my web site [Andres Rojano](http://andresrojano.info)
