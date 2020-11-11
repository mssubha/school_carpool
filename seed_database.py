
"""Script to seed database."""

import os #module from Python’s standard library, code related to working with your computer’s operating system.
from datetime import datetime #We’ll use datetime.strptime to turn a string into a Python datetime object.

import server
import model
import crud
import csv



# os.system('dropdb ratings')
# os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/user.csv', newline='') as user_file:
    users = csv.reader(user_file, delimiter=',')
    next(users) # to skip the header
    for user in users:
        email, password, household1, household2, phone_number, address_street, address_city, address_state, address_zip = user
  
        crud.create_user(email, password, household1, household2, phone_number, 
                address_street, address_city, address_state, address_zip)


with open('data/cars.csv', newline='') as user_file:
    cars = csv.reader(user_file, delimiter=',')
    next(cars) # to skip the header
    for car in cars:
        email,car_make,car_model,license_plate,smoking,pets,seats = car
        crud.create_user_car(email,car_make,car_model,license_plate,smoking,pets,seats)


with open('data/children.csv', newline='') as user_file:
    children = csv.reader(user_file, delimiter=',')
    next(children) # to skip the header
    for child in children:
        email, childname, grade = child
        crud.create_user_child(email, childname, grade)