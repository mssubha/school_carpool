"""Server for movie carpool app."""
from flask import (Flask, render_template, request, flash, session,
                   redirect,jsonify)
from datetime import datetime
from model import connect_to_db
import crud
import userqueries
from jinja2 import StrictUndefined
import os

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View Homepage"""
    return render_template('homepage.html',message ="")
 
  
@app.route('/create_user', methods=['POST'])
def create_user():
    """ Create New User with user, car and child information """
    email = request.form.get('email')
    password = request.form.get('password')
    household1 = request.form.get('name1')
    household2 = request.form.get('name2')
    phone_number = request.form.get('phone')
    address_street = request.form.get('street')
    address_city = request.form.get('city')
    address_state = request.form.get('state')
    address_zip = request.form.get('zipcode')
    crud.create_user(email, password, household1, household2, phone_number, 
                address_street, address_city, address_state, address_zip)

    car_make = request.form.get("carmake")
    car_model = request.form.get("carmodel")
    license_plate = request.form.get("licenseplate")
    seats = request.form.get("carpoolseats")
    smoking = request.form.get("smoking")
    pets = request.form.get("pets")
    crud.create_user_car(email,car_make,car_model,license_plate,smoking,pets,seats)

    childname = request.form.get("childname")
    grade = request.form.get("childgrade")
    crud.create_user_child(email, childname, grade)
    

    flash ("User Successfully Created. Login to Continue")
    return redirect('/') 


@app.route('/user', methods=['POST'])   
def user_login():
    """ Validate Login and Display User Page"""
    if (request.form.get('action') == 'login'):
        email = request.form.get('username')
        password = request.form.get('password')
        existing_user = crud.get_user_by_email(email)
    
        if (existing_user == None):
            # flash("User not found. Create an account")
            return render_template('homepage.html', message = "User not found. Create an account" ) 
        elif (crud.check_login_details(email,password) == False):
            # flash ("Invalid Password")
            return render_template('homepage.html', message = "Invalid Password") 
        else:
            session['username'] = email
            buddies = userqueries.get_user_buddies(email)
            
            return render_template('user.html',buddies=buddies,number = len(buddies))
    else:
        return render_template('newuser.html')


@app.route("/api/carpoolers")
def carpoolers_info():
    """JSON information about carpoolers."""

    carpoolers = [
        {
            "user_id": carpooler.user_id,
            "name": carpooler.household1,
            "street": carpooler.address_street,
            "city": carpooler.address_city,
            "phone": carpooler.phone_number,
            "email": carpooler.email,
            "userLat": carpooler.address_latitude,
            "userLong": carpooler.address_longitude,
        }
        for carpooler in userqueries.get_user_buddies(session['username'])
        # for carpooler in userqueries.get_user_buddies('6tester6@test.com')
    ]

    return jsonify(carpoolers)


@app.route("/api/request_peson")
def request_person_info():
    request_user = crud.get_user_by_id(session['send_request_to'])
    login_user = crud.get_user_by_email(session['username'])
    a = session['send_request_to']
    b = session['username']
    print (f'send_to {a} and user in {b}')
    carpoolers = [
        {
            "user_id": request_user.user_id,
            "name": request_user.household1,
            "street": request_user.address_street,
            "city": request_user.address_city,
            "phone": request_user.phone_number,
            "email": request_user.email,
            "userLat": request_user.address_latitude,
            "userLong": request_user.address_longitude,
        },
        {
            "user_id": login_user.user_id,
            "name": login_user.household1,
            "street": login_user.address_street,
            "city": login_user.address_city,
            "phone": login_user.phone_number,
            "email": login_user.email,
            "userLat": login_user.address_latitude,
            "userLong": login_user.address_longitude,
        }
    ]

    return jsonify(carpoolers)


@app.route("/api/search_carpoolers")
def search_carpoolers_info():
    """JSON information about carpoolers."""

    # a = session['smoking_preference']
    # b = session['pets_preference']
    # print (f'Smoking is {a}')
    # print (f'Pets is {b}')

    carpoolers = [
        {
            "user_id": carpooler.user_id,
            "name": carpooler.household1,
            "street": carpooler.address_street,
            "city": carpooler.address_city,
            "phone": carpooler.phone_number,
            "email": carpooler.email,
            "userLat": carpooler.address_latitude,
            "userLong": carpooler.address_longitude,
        }
        for carpooler in  userqueries.get_carpool_closeby_filter(session['username'],session['smoking_preference'],session['pets_preference'])
    ]

    return jsonify(carpoolers)


@app.route('/search_filter_carpool' , methods=['POST'])
def search_carpool_filter():
    session['smoking_preference'] = 0
    session['pets_preference'] = 0
    smoking = 0
    pets = 0
    
    print (request.form.get('search_smoking'))
    print (request.form.get('search_pets'))

    if (request.form.get('search_smoking') == 'YES'):
        smoking = 1
        session['smoking_preference'] = 1
    
    if (request.form.get('search_pets') == 'YES'):
        pets = 1
        session['pets_preference'] = 1
    
    # session['smoking_preference'] = smoking
    # session['pets_preference'] = pets
    carpoolers = userqueries.get_carpool_closeby_filter(session['username'],smoking,pets)
    return render_template('search.html', carpoolers = carpoolers)


@app.route('/search_carpool')
def search_carpool():
    carpoolers = userqueries.get_carpool_closeby(session['username'])
    return render_template('search.html', carpoolers = carpoolers)


@app.route('/individual_request', methods =['POST'])
def display_individual_user():
    request_user_id=request.form.get('carpoolrequest')
    request_user = crud.get_user_by_id(request_user_id)
    request_user_children = request_user.children
    login_user = crud.get_user_by_email( session['username'])
    session['send_request_to'] = request_user_id
    return render_template('send_request.html', request_user = request_user, request_user_children = request_user_children,login_user=login_user  )


@app.route('/send_request', methods=['POST'])
def send_request():
    """ Send a carpool request to a carpooler livnig near the user"""
    notes = request.form.get('request_note')

    login_user = crud.get_user_by_email(session['username'])
    from_user = login_user.user_id
    to_user = session['send_request_to']
    child_id = login_user.children[0].child_id
    request_note = notes
    request_datetime = datetime.now() 
    print (notes)
    crud.create_request(from_user,to_user,child_id,request_note,"","S",request_datetime)

    buddies = userqueries.get_user_buddies(session['username'])
    return render_template('user.html',buddies=buddies)
   

@app.route('/accept_deny_request', methods=['POST'])
def show_requests():
    """ Show all the requests that a user has recieved"""
    carpoolers = userqueries.get_requests_recieved(session['username'])
    return render_template('requests.html', carpoolers = carpoolers)


@app.route('/individual_accept_deny', methods= ['POST'])
def accept_deny_request():
    """ User can accept or deny a request """
    request_user_id=request.form.get('carpoolrequest')
    request_user = crud.get_user_by_id(request_user_id)
    request_user_children = request_user.children
    login_user = crud.get_user_by_email( session['username'])
    session['accept_deny_userid'] = request_user_id
    return render_template('accept_deny.html', request_user = request_user, request_user_children = request_user_children,login_user=login_user)


@app.route('/logout') 
def logout():  
    return render_template('logout.html')


# @app.route('/accept_deny_individual', methods= ['POST'])
# def accept_deny_individual_request():
#     accept_or_deny = request.form.get('send_request')
#     if (accept_or_deny == "Accept"):
#         request_code = "A"
#     else:
#         request_code = "D"

#     notes = request.form.get('request_note')

#     login_user = crud.get_user_by_email(session['username'])
#     from_user = login_user.user_id
#     to_user = session['accept_deny_userid']
#     child_id = login_user.children[0].child_id
#     request_note = notes
#     request_datetime = datetime.now() 
#     print (notes)
#     crud.create_request(from_user,to_user,child_id,request_note,"","S",request_datetime)

#     buddies = userqueries.get_user_buddies(session['username'])
#     return render_template('user.html',buddies=buddies)
   


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)