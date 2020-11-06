""" CRUD operations"""

from model import db, User, Car, Child, Request, connect_to_db
from datetime import datetime


def create_user(email, password, household1, household2, phone_number, 
                address_street, address_city, address_state, address_zip):
    """Create and return a new user."""

    user = User(email=email, password=password, household1=household1,
                household2=household2, phone_number=phone_number,
                address_street=address_street, address_city=address_city,
                address_state=address_state,address_zip=address_zip)

# create_user("user1@test.com","123","User1","User2","415-340-4344","3 Adrian Way","San rafael","CA","94903")
#     db.session.add(user)
    db.session.commit()

    return user

# test_user = create_user("test@test.test","123")

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

if __name__ == '__main__':
    from server import app
    connect_to_db(app)