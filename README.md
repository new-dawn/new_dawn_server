# New Dawn Server Repo
[![Build Status](https://travis-ci.org/new-dawn/new_dawn_server.svg?branch=master)](https://travis-ci.org/new-dawn/new_dawn_server)

## Setup
1. Clone the repo to your local machine by running `git clone https://github.com/tangziyi001/new_dawn_server.git`
2. Download virtualenv
3. Run `virtualenv new_dawn` to create a virtual env
4. Activate your virtual env by running `source new_dawn/bin/activate`
5. Run `pip3 install -r requirements.txt` to install dependencies

## Run Server & Test API
1. Run local server `python3 manage.py runserver`.
2. In another terminal session, use `curl` to GET/POST your request.

### Example
* Registration
```
curl --dump-header - -H "Content-Type: application/json" -X POST --data '{"first_name": "ziyi", "last_name": "tang"}' http://localhost:8000/api/v1/register/
``` 
You should get an error message from server since the required fields are missing. Fill in required fields will let you successfully register a user:
```
curl --dump-header - -H "Content-Type: application/json" -X POST --data '{"first_name": "ziyi", "last_name": "tang", "birthday": "1800-01-01", "password": "manman", "phone_number": "+11111111111", "username": "goodman", "gender": "M"}' http://localhost:8000/api/v1/register/
```
Then you should see a success message:
```
HTTP/1.1 201 Created
Date: Mon, 03 Dec 2018 03:33:22 GMT
Server: WSGIServer/0.2 CPython/3.6.7
Content-Type: application/json
Location: /api/v1/register/7/
Vary: Accept
X-Frame-Options: SAMEORIGIN
Content-Length: 381

{"birthday": "1800-01-01", "date_joined": "2018-12-02T22:33:22.203670", "email": "", "first_name": "ziyi", "gender": "M", "id": 7, "is_active": true, "is_staff": false, "is_superuser": false, "last_login": null, "last_name": "tang", "password": "pbkdf2_sha256$120000$EZGzO2YmhkK6$jgsvSXMXV41gyEVDsWQAgxkn/sT0W+xnZvMYUkNY8DA=", "phone_number": "+11111111111", "username": "goodman"}
```
Feel free to play with different invalid input to see how the server returns error message.
Except for required fields, there are some optional fields that you can lookup from `users/api/resources.py`

## Dev Basic
* Make sure to re-do the step 4 above before coding. After dev, run `deactivate` to exit the virtual env.
* Please create your own branch by running `git branch <yourname>` and run `git checkout <yourname>` before development. Run `git pull origin master` frequently to make sure that you are in sync with the master branch.
* Commit and push your work by running `git push origin <yourname>` instead of master.
* Send pull request for code review before merging.

## Dev Data Model
* Data models are stored in directories such as `users/models.py`. Make changes you want in `models.py`.
* Run `python3 manage.py makemigrations` and `python3 manage.py migrate`. If everything works fine, you should be able to see the following messages:
```
(new_dawn) TZY-Mac:new_dawn_server Tang$ python3 manage.py makemigrations
Migrations for 'users':
  new_dawn_server/users/migrations/0002_remove_account_nationality.py
    - Remove field nationality from account
(new_dawn) TZY-Mac:new_dawn_server Tang$ python3 manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, users
Running migrations:
  Applying users.0002_remove_account_nationality... OK
(new_dawn) TZY-Mac:new_dawn_server Tang$ 
```
* You should be able to see migration files generated in `migrations/`. Commit all generated changes and push to your branch
