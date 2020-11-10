
"""Script to seed database."""

import os #module from Python’s standard library, code related to working with your computer’s operating system.
from datetime import datetime #We’ll use datetime.strptime to turn a string into a Python datetime object.

import crud
import model
import server
import csv

# os.system('dropdb ratings')
# os.system('createdb ratings')

# model.connect_to_db(server.app)
# model.db.create_all()

# Load movie data from JSON file
with open('data/user.csv', newline='') as user_file:
    users = csv.reader(user_file, delimiter=',')
    for user in users:
        print(user)

