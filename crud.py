""" CRUD operations"""

from model import db, User, Car, Child, Request, connect_to_db
from datetime import datetime


def create_user(email, password, household1, household2, phone_number, 
                address_street, address_city, address_state, address_zip):
    """Create and return a new user."""

    user = User(email=email, password=password, household1=household1,
                household2=household2, phone_number=phone_number,
                address_street=address_street, address_city=address_city,
                address_state=address_state,address_zip=address_zip,address_latitude =0,
                address_longitude =0)

# User(email = 'user3@test.com',password = '123', household1 = 'User3',
# ... household2 = 'User2', phone_number = '415-340-2334',
# ... address_street = '3 Adrian Way',address_city ='San Francisco',
# ... address_state = 'CA',address_zip ='94903',address_latitude=0,address_longitude =0)

# create_user("user15@test.com","help","Usertets","User2","415-340-4224","21 Labrea","Foster City","CA","94253")
    
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

def create_user_car(user_id,car_make,car_model,license_plate,smoking,pets,seats):

    car = Car(user_id = user_id,car_make = car_make,car_model = car_model,
              license_plate = license_plate, smoking = smoking,
              pets = pets, seats = seats)

    db.session.add(car)
    db.session.commit()

    return car

def get_cars():
    """ Return all cars"""
    return Car.query.all()

def get_car_by_id(user_id):
    """ Return user by id"""
    return Car.query.get(user_id)

if __name__ == '__main__':
    from server import app
    connect_to_db(app)

    # pg_dump carpool > carpool.sql