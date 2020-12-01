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

def distance_between_addresses(user_geo, carpooler_geo):
    query = db.session.query(func.ST_DistanceSphere(user_geo, carpooler_geo))
    for row in query:
        distance_in_miles = row[0]/1609.34
    return (round(distance_in_miles,2))
# Select ST_Distance_Sphere('01010000008C1D43B6629E5EC0A85C3C17A1FD4240','01010000004CCC0E4C499E5EC05B2DB0C744FE4240')/1609.34 as dist;

def get_carpool_closeby(email, distance = 25):
        """Return all address within a given distance from the user's address."""
        # ST_DistanceSphere compares distance in meters. 1 Mile = 1609.34 meters.
        distance_in_meters = distance * 1609.34
        user_geo = crud.get_user_geo(email)
        # return User.query.filter(func.ST_DistanceSphere(User.address_geo, user_geo) < distance_in_meters).all()
        all_users =  User.query.filter(func.ST_DistanceSphere(User.address_geo, user_geo) < distance_in_meters).all()
        buddies = get_user_buddies(email)
        
        buddies_email= []
        for buddy in range(len(buddies)):
            buddies_email.append(buddies[buddy][6])

        return_users = []

        for user in all_users:
            if (user.email not in buddies_email and user.email != email):
                return_users.append(user)
        return(return_users)




def get_carpooler_preference(carpooler_id):
    """ Return the car details for a user """
    return Car.query.get(carpooler_id)


def get_carpool_closeby_filter(email,smoking,pets,distance):
    """Return all address within a given distance from the user's address."""
    filtered_carpoolers = []
    carpoolers_closeby = get_carpool_closeby(email,distance)
    
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


    # SELECT request_id, user_id, household1, address_street, address_city, address_state , phone_number, email,
    #          address_latitude, address_longitude
    #          FROM users, requests
    #          WHERE users.user_id = requests.from_user
    #          AND request_status = 'S' and to_user = 2
