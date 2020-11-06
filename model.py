"""Models for carpool app."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func
from geoalchemy2 import (Geometry, Geography)

db = SQLAlchemy()

class Parent(db.Model):
    """A parent, address, email, password, address and its geospatial data."""

    __tablename__ = "parents"

    parent_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(30),nullable=False, unique=True)
    password = db.Column(db.String(30),nullable=False)
    household1 = db.Column(db.String(50),nullable=False)
    household2 = db.Column(db.String(50))
    phone_number = db.Column(db.String(15),nullable=False)
    address_street = db.Column(db.String(30),nullable=False)
    address_city = db.Column(db.String(30),nullable=False)
    address_state = db.Column(db.String(30),nullable=False)
    address_zip = db.Column(db.String(10),nullable=False)
    address_latitude = db.Column(db.Float)
    address_longitude = db.Column(db.Float)
    # address_geo = db.Column(Geometry(geometry_type="POINT"))
    
    # car = db.relationship('Car')

    def __repr__(self):
        return f'<parent_id {self.parent_id} email{self.email}' #', address_geo{self.address_geo}'

class Car(db.Model):
    """Details of a car owned by a parent """

    __tablename__ = "cars"

    car_id  = db.Column(db.Integer, primary_key=True, autoincrement=True)
    parent_id = db.Column(db.Integer,db.ForeignKey('parents.parent_id'))
    car_make = db.Column(db.String(20))
    car_model = db.Column(db.String(20))
    license_plate = db.Column(db.String(20), nullable=False)
    smoking = db.Column(db.Boolean)
    pets = db.Column(db.Boolean)
    seats = db.Column(db.Integer, nullable=False)

    # parent = db.relationship('Parent')
    # children = db.relationship('Child')

    def __repr__(self):
        return f'<car_id {self.car_id} parent_id{self.parent_id}, license_plate{self.license_plate}'


class Child(db.Model):
    """Details of a car owned by a parent """

    __tablename__ = "children"

    child_id  = db.Column(db.Integer, primary_key=True, autoincrement=True)
    parent_id = db.Column(db.Integer,db.ForeignKey('parents.parent_id'))
    name = db.Column(db.String(50))
    grade = db.Column(db.Integer)

    # parent = db.relationship('Parent')

    def __repr__(self):
        return f'<child_id {self.child_id} parent_id{self.parent_id}, name{self.name}'



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