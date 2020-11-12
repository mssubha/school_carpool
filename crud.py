""" CRUD operations"""

from model import db, User, Car, Child, Request, connect_to_db
from datetime import datetime
import googlemaps
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from geoalchemy2 import Geometry, Geography

def create_user(email, password, household1, household2, phone_number, 
                address_street, address_city, address_state, address_zip):
    """Create and return a new user."""
    # api_key = secret.google_api_key
    api_key = os.environ['google_api_key'] 
    gmaps_client = googlemaps.Client(api_key)
    address = (f'{address_street} {address_city} {address_state}')
    geocode_result = gmaps_client.geocode(address)
    result = geocode_result[0]
    latitude = result['geometry']['location']['lat']
    longitude = result['geometry']['location']['lng']

    geo=func.ST_Point(longitude, latitude)

    user = User(email=email, password=password, household1=household1,
                household2=household2, phone_number=phone_number,
                address_street=address_street, address_city=address_city,
                address_state=address_state,address_zip=address_zip,address_latitude =latitude,
                address_longitude =longitude,address_geo=geo)

    db.session.add(user)
    db.session.commit()

    return user

def get_users():
    """ Return all users"""
    return User.query.all()

def get_user_by_id(user_id):
    """ Return user by id"""
    return User.query.get(user_id)

def get_user_by_email(email):
    """ Return user by email."""
    # Search in db email. If matches any give User info
    # if doesn't return None
    return User.query.filter(User.email == email).first()

def get_user_geo(email):
    user = get_user_by_email(email)
    geo = user.address_geo
    return(geo)

def check_login_details(email,password):
    login_user = get_user_by_email(email)
    return (login_user.password == (password))


def create_user_car(email,car_make,car_model,license_plate,smoking,pets,seats):
    """ Enter car details of the user """
    user = get_user_by_email(email)
    user_id = user.user_id
    car = Car(user_id = user_id,car_make = car_make,car_model = car_model,
              license_plate = license_plate, smoking = int(smoking),
              pets = int(pets), seats = int(seats))

    db.session.add(car)
    db.session.commit()

    return car

def get_cars():
    """ Return all cars"""
    return Car.query.all()

def get_car_by_id(user_id):
    """ Return user by id"""
    return Car.query.get(user_id)



def create_user_child(email, childname, grade):
    """ Create a record for each child of the user """
    user = get_user_by_email(email)
    user_id = user.user_id

    child = Child(user_id = user_id,name = childname,grade = grade)

    db.session.add(child)
    db.session.commit()

    return child

def get_children():
    """ Return all cars"""
    return Child.query.all()

def get_children_of_user(user_id):
    """ Return user by id"""
    return Child.query.filter_by(user_id=user_id).all()


def create_request(from_user,to_user,child_id,request_note,decision_note,request_status,request_datetime):

# datetime.strptime('2011-01-21 02:37:21', '%Y-%m-%d %H:%M:%S')

    if (request_status == 'S'):
        request_datetime =  datetime.now() #dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        response_dateime = None
    else:
        response_dateime =   datetime.now()


    request = Request(from_user = from_user,
    to_user = to_user,
    child_id = child_id,
    request_note = request_note,
    decision_note = decision_note,
    request_status = request_status,
    request_datetime=request_datetime,
    response_dateime = response_dateime)

    db.session.add(request)
    db.session.commit()

    return request
 
# >>> from datetime import datetime
# >>> create_request(1,2,3,"Test CRUD request","","S",datetime.now())

if __name__ == '__main__':
    from server import app
    connect_to_db(app)

    # pg_dump carpool > carpool.sql
    # psql carpool < carpool.sql