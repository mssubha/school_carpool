""" CRUD operations"""

from model import db, User, Car, Child, Request, connect_to_db
from datetime import datetime
import googlemaps
import os
import crud
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
# from geoalchemy2 import Geometry, Geography

def get_user_buddies(email):
    user_id = crud.get_user_by_email(email).user_id
    sql = """SELECT user_id, household1, address_street, address_city, address_state , phone_number, email,
             address_latitude, address_longitude
             FROM users 
             WHERE users.user_id in 
             (SELECT from_user from requests where request_status = 'A' and to_user = :user_id)
             OR users.user_id in 
             (SELECT to_user from requests where request_status = 'A' and from_user = :user_id)""" 


    buddies = db.session.execute(sql, {"user_id": user_id}).fetchall()
    return(buddies)


def static_map(email):
   api_key = os.environ['google_api_key'] 
   return("http://maps.google.com/maps/api/staticmap?center=Brooklyn+Bridge,New+York,NY&zoom=14&size=512x512&maptype=roadmap&markers=color:blue|label:S|40.702147,-74.015794&markers=color:green|label:G|40.711614,-74.012318&markers=color:red|label:C|40.718217,-73.998284&sensor=false&key="+api_key)


def get_carpool_closeby(email):
        """Return all address within a given distance from the user's address."""
        # ST_DistanceSphere compares distance in meters. 1 Mile = 1609.34 meters.
        user_geo = crud.get_user_geo(email)
        return User.query.filter(func.ST_DistanceSphere(User.address_geo, user_geo) < 804.67).all()


def get_carpooler_preference(carpooler_id):
    """ Return the car details for a user """
    return Car.query.get(carpooler_id)


def get_carpool_closeby_filter(email,smoking,pets):
    """Return all address within a given distance from the user's address."""
    filtered_carpoolers = []
    carpoolers_closeby = get_carpool_closeby(email)
    
    if (smoking == 0 and pets == 0):
        return carpoolers_closeby
    
    if (smoking == 1 and pets == 1):
        for carpooler in carpoolers_closeby:
            carpooler_preference = get_carpooler_preference(carpooler.user_id)
            if (carpooler_preference.pets == False and carpooler_preference.smoking == False):
                filtered_carpoolers.append(carpooler)
        return filtered_carpoolers

    if (smoking == 0 and pets == 1):
        for carpooler in carpoolers_closeby:
            carpooler_preference = get_carpooler_preference(carpooler.user_id)
            if (carpooler_preference.pets == False):
                filtered_carpoolers.append(carpooler)
        return filtered_carpoolers

    if (smoking == 1 and pets == 0):
        for carpooler in carpoolers_closeby:
            carpooler_preference = get_carpooler_preference(carpooler.user_id)
            if (carpooler_preference.smoking == False):
                filtered_carpoolers.append(carpooler)
        return filtered_carpoolers


def get_requests_recieved(email):
    user_id = crud.get_user_by_email(email).user_id
    sql = """SELECT user_id, household1, address_street, address_city, address_state , phone_number, email,
             address_latitude, address_longitude
             FROM users 
             WHERE users.user_id in 
             (SELECT from_user from requests where request_status = 'S' and to_user = :user_id)"""
  
    carpool_requests = db.session.execute(sql, {"user_id": user_id}).fetchall()
    return(carpool_requests)

if __name__ == '__main__':
    from server import app
    connect_to_db(app)

    # pg_dump carpool > carpool.sql
    # psql carpool < carpool.sql