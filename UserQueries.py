""" CRUD operations"""

from model import db, User, Car, Child, Request, connect_to_db
from datetime import datetime
import googlemaps
import os
import secret
import crud
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from geoalchemy2 import Geometry, Geography

def get_user_buddies(email):
    user_id = crud.get_user_by_email(email).user_id
    sql = """SELECT household1, address_street, address_city, address_state , phone_number, email 
             FROM users 
             WHERE users.user_id in 
             (SELECT from_user from requests where request_status = 'A' and to_user = :user_id)
             OR users.user_id in 
             (SELECT to_user from requests where request_status = 'A' and from_user = :user_id)""" 


    buddies = db.session.execute(sql, {"user_id": user_id}).fetchall()
    return(buddies)
    
    # return (User.query.filter(User.email == email).all())
    
                                       
# select household1, address_street, address_city, address_state , phone_number, email from users where users.user_id in (
# dbcarpool(# 1,6);

# select household1, address_street, address_city, address_state , phone_number, email 
# from users 
# where users.user_id in (select from_user from requests where request_status = 'A' and to_user = 2) 
# or users.user_id in (select to_user from requests where request_status = 'A' and from_user = 2);


# dbcarpool=# select household1, address_street, address_city, address_state , phone_number, email from users where users.user_id in (
# select from_user from requests where request_status = 'A' and to_user = 2) or users.user_id in (
# dbcarpool(# select to_user from requests where request_status = 'A' and from_user = 2);

# from sqlalchemy import text

# sql = text('select name from penguins')
# result = db.engine.execute(sql)
# names = [row[0] for row in result]
# print names


def check_login_details(email,password):
    login_user = get_user_by_email(email)
    return (login_user.password == (password))

if __name__ == '__main__':
    from server import app
    connect_to_db(app)

    # pg_dump carpool > carpool.sql
    # psql carpool < carpool.sql