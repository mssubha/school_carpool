"""Models for carpool app."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func
from geoalchemy2 import (Geometry, Geography)

db = SQLAlchemy()

class User(db.Model):
    """A parent, address, email, password, address and its geospatial data."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String,nullable=False, unique=True)
    password = db.Column(db.String,nullable=False)
    household1 = db.Column(db.String,nullable=False)
    household2 = db.Column(db.String)
    phone_number = db.Column(db.String,nullable=False)
    address_street = db.Column(db.String,nullable=False)
    address_city = db.Column(db.String,nullable=False)
    address_state = db.Column(db.String,nullable=False)
    address_zip = db.Column(db.String,nullable=False)
    address_latitude = db.Column(db.Float)
    address_longitude = db.Column(db.Float)
    address_geo = db.Column(Geometry(geometry_type="POINT"))
    
    car = db.relationship('Car')
    children = db.relationship('Child')
    requests = db.relationship('Request')

    def __repr__(self):
        return f'<user_id {self.user_id} email{self.email}, address_geo{self.address_geo}'

class Car(db.Model):
    """Details of a car owned by a parent """

    __tablename__ = "cars"

    car_id  = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.user_id'))
    car_make = db.Column(db.String)
    car_model = db.Column(db.String)
    license_plate = db.Column(db.String, nullable=False)
    smoking = db.Column(db.Boolean)
    pets = db.Column(db.Boolean)
    seats = db.Column(db.Integer, nullable=False)

    users = db.relationship('User')

    def __repr__(self):
        return f'<car_id {self.car_id} user_id{self.user_id}, license_plate{self.license_plate}'


class Child(db.Model):
    """Details of Children of the user """

    __tablename__ = "children"

    child_id  = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.user_id'))
    name = db.Column(db.String)
    grade = db.Column(db.Integer)

    users = db.relationship('User')

    def __repr__(self):
        return f'<child_id {self.child_id} user_id{self.user_id}, name{self.name}'


class Request(db.Model):
    """ Accept of Denial of a carpool request """

    __tablename__ = "requests"

    request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    from_user = db.Column(db.Integer,db.ForeignKey('users.user_id'))
    to_user = db.Column(db.Integer,db.ForeignKey('users.user_id'))
    child_id = db.Column(db.Integer,db.ForeignKey('children.child_id'))
    request_note = db.Column(db.Text)
    decision_note = db.Column(db.Text)
    request_status = db.Column(db.String)
    request_datetime =  db.Column(db.DateTime)
    response_dateime =  db.Column(db.DateTime)

    users = db.relationship('User')

    def __repr__(self):
        return f'<request_id {self.request_id} from_user{self.from_user}, to_user{self.to_user}, request_status{self.request_status}'



def connect_to_db(flask_app, db_uri='postgresql:///carpool', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.
    connect_to_db(app)
    # CREATE EXTENSION postgis; - run this inside the database
    db.create_all()