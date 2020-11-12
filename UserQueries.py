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
    sql = """SELECT household1, address_street, address_city, address_state , phone_number, email 
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

# select household1, address_street, address_city, address_state , phone_number, email 
# from users 
# where users.user_id in (select from_user from requests where request_status = 'A' and to_user = 2) 
# or users.user_id in (select to_user from requests where request_status = 'A' and from_user = 2);


if __name__ == '__main__':
    from server import app
    connect_to_db(app)

    # pg_dump carpool > carpool.sql
    # psql carpool < carpool.sql