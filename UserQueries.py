""" CRUD operations"""

from model import db, User, Car, Child, Request, connect_to_db
from datetime import datetime
import googlemaps
import os
import secret
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from geoalchemy2 import Geometry, Geography

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

def check_login_details(email,password):
    login_user = get_user_by_email(email)
    return (login_user.password == (password))

def get_cars():
    """ Return all cars"""
    return Car.query.all()

def get_car_by_id(user_id):
    """ Return user by id"""
    return Car.query.get(user_id)


def get_children():
    """ Return all cars"""
    return Child.query.all()

def get_children_of_user(user_id):
    """ Return user by id"""
    return Child.query.filter_by(user_id=user_id).all()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)

    # pg_dump carpool > carpool.sql
    # psql carpool < carpool.sql