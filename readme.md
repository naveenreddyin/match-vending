# Vendor Machine API for Match
## Description

Design an API for a vending machine, allowing users with a “seller” role to add, update or remove products, while users with a “buyer” role can deposit coins into the machine and make purchases. Your vending machine should only accept 5, 10, 20, 50 and 100 cent coins

## Installation and running the app

```bash
$ pip install --user pipenv
$ git clone https://github.com/naveenreddyin/match-vending.git
$ cd match-vending
$ cp .env.exmaple .env #don't forget to update the DB credential
$ pipenv shell
$ pipenv install
$ pipenv run python manage.py runserver 0.0.0.0:8002  # port or host could be anything
$ pipenv run python manage.py createsuperuser # create super user to login to admin panel and docs etc.
```
## Test 

```bash
$ pipenv run pytest
```

## Documentation
Assuming super user is created already and logged in via url ```http://localhost:8002/admin/``` and then navigate to ```http://localhost:8002/api-docs/``` for Swagger docs.

## Technology Stack
* **Language**: [python] 3.9.9
* **Web Framework**: [Django](https://djangoproject.com) 3.2
* **Database**: [Sqlite]

## Notes:
* CRUD endpoints for Products are done.
* User roles are supported.
* User login and registration are done.
* Multiple login sessions for user is handled. (Bonus point).
* Token based auth.
* Buy and deposit endpoints are done.
* Logout all endpoint done.
* around 40+ tests.