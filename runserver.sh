#!/bin/sh

# Author: Ziyi Tang
# Description: A script to run Django server with environment and db setup

echo "Setup OS Environment: Please make sure that you are already in your virtualenv, and has ran 'pip3 install -r requirements.txt'"

echo "--- Create testing user: {username: testadmin, password: admintest}"
export SUPER_USER_NAME="testadmin"
export SUPER_USER_PASSWORD="admintest"
export SUPER_USER_EMAIL="superemail"

echo "--- DB Migration"
python3 manage.py migrate

echo "--- Pre-run Commands"
python3 manage.py create_super_user

echo "--- Run Server"
python3 manage.py runserver
