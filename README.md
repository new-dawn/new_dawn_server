# New Dawn Server Repo
[![Build Status](https://travis-ci.com/tangziyi001/new_dawn_server.svg?token=UWU238fD4jfedxeMH6HU&branch=master)](https://travis-ci.com/tangziyi001/new_dawn_server)

## Setup
1. Clone the repo to your local machine by running `git clone https://github.com/tangziyi001/new_dawn_server.git`
2. Download virtualenv
3. Run `virtualenv new_dawn` to create a virtual env
4. Activate your virtual env by running `source new_dawn/bin/activate`
5. Run `pip install -r requirements.txt` to install dependencies

## Dev Basic
* Make sure to re-do the step 4 above before coding. After dev, run `deactivate` to exit the virtual env.
* Please create your own branch by running `git branch <yourname>` and run `git checkout <yourname>` before development. Run `git pull origin master` frequently to make sure that you are in sync with the master branch.
* Commit and push your work by running `git push origin <yourname>` instead of master.
* Send pull request for code review before merging.

## Dev Data Model
* Data models are stored in directories such as `users/models.py`. Make changes you want in `models.py`.
* Run `python manage.py makemigrations` and `python manage.py migrate`. If everything works fine, you should be able to see the following messages:
```
(new_dawn) TZY-Mac:new_dawn_server Tang$ python manage.py makemigrations
Migrations for 'users':
  new_dawn_server/users/migrations/0002_remove_account_nationality.py
    - Remove field nationality from account
(new_dawn) TZY-Mac:new_dawn_server Tang$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, users
Running migrations:
  Applying users.0002_remove_account_nationality... OK
(new_dawn) TZY-Mac:new_dawn_server Tang$ 
```
* You should be able to see migration files generated in `migrations/`. Commit all generated changes and push to your branch
