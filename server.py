"""Server for movie carpool app."""
from flask import (Flask, render_template, request, flash, session,
                   redirect,jsonify)
from datetime import datetime
from model import connect_to_db
import crud
import userqueries
import send_message
from jinja2 import StrictUndefined
import os

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


"""Home Page"""
@app.route('/')
def homepage():
    """View Homepage"""
    return render_template('homepage.html',message ="")
 

"""Create New User"""
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


"""Login"""
@app.route('/login', methods=['POST'])   
def user_login():
    """ Validate Login and Display User Page"""
    if (request.form.get('action') == 'login'):
        email = request.form.get('username')
        password = request.form.get('password')
        existing_user = crud.get_user_by_email(email)
        
        if (existing_user == None):
            return render_template('homepage.html', message = "User not found. Create an account" ) 
        elif (crud.check_login_details(email,password) == False):
            return render_template('homepage.html', message = "Invalid Password") 
        else:
            session['user_id'] =existing_user.user_id
            session['username'] = email
            buddies = userqueries.get_user_buddies(email)
            if len(buddies) > 0:
                buddy = crud.get_user_by_id(buddies[0].user_id)
                session['buddy_phone']= buddy.phone_number
                session['buddy_id'] = buddy.user_id
                # request_user_children = crud.get_user_by_id(buddies[0].user_id).children
                request_user_children = buddy.children
            else:
                request_user_children = []
            return render_template('user.html',buddies=buddies,number = len(buddies),request_user_children=request_user_children)
    else:
        return render_template('newuser.html')

""" Cancel Carpool or send additional message"""
@app.route('/send_additional_message', methods=['POST'])
def send_additional_message():
    message = request.form.get('additional_note')
    action = request.form.get('send_message')
    if (action == "cancel"):
        print(session['user_id'])    
        print(session['buddy_id'])
        userqueries.cancel_carpool(session['user_id'],session['buddy_id'] ,message)
        carpoolers = userqueries.get_carpool_closeby_filter(session['username'],0,0,25,0)
        user_geo = crud.get_user_by_email(session['username']).address_geo
        for carpooler in carpoolers:
            carpooler.address_longitude = userqueries.distance_between_addresses(user_geo,carpooler.address_geo)
            carpooler.latitude = carpooler.car[0].seats
        # send_message.send_message(session['buddy_phone'],message)
        flash (f"Message successfully sent to {session['buddy_phone']} ")
        return render_template('search.html', carpoolers = carpoolers)
    else:
        send_message.send_message(session['buddy_phone'],message)
        flash (f"Message successfully sent to {session['buddy_phone']} ")
        return redirect('/') 
            

""" Return JSON of carpool buddies """
@app.route("/carpoolers/json")
def carpoolers_info():
    """JSON information about carpool buddies."""

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
        for carpooler in userqueries.get_request_recieved_map(session['username'])
    ]

    return jsonify(carpoolers)

@app.route("/requests/json")
def requests_info():
    """JSON information about carpool buddies."""

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
        for carpooler in userqueries.get_requests_recieved(session['username'])
    ]

    return jsonify(carpoolers)



@app.route("/back_user_page")
def display_user_page():
    return render_template('user.html',buddies=[],number = 0,request_user_children=[])

@app.route("/back_all_carpoolers")
def display_all_carpoolers():
    all_carpoolers= []
    all_carpoolers = return_all_carpoolers()
    return render_template('search.html', carpoolers = all_carpoolers)


def return_all_carpoolers():
    session['smoking_preference'] = 0
    session['pets_preference'] = 0
    session['distance'] = 25
    session['grade'] = 0
    carpoolers = userqueries.get_carpool_closeby_filter(session['username'],0,0,25,0)
    user_geo = crud.get_user_by_email(session['username']).address_geo
    for carpooler in carpoolers:
        carpooler.address_longitude = userqueries.distance_between_addresses(user_geo,carpooler.address_geo)
        carpooler.latitude = carpooler.car[0].seats
    
    return  carpoolers

""" Display all carpoolers to whom you can send request"""
@app.route('/all_carpoolers' , methods=['POST'])
def search_all_carpool():
    """ List all carpoolers available without any filter"""
    all_carpoolers= []
    all_carpoolers = return_all_carpoolers()
    return render_template('search.html', carpoolers = all_carpoolers)

    # session['smoking_preference'] = 0
    # session['pets_preference'] = 0
    # session['distance'] = 25
    # session['grade'] = 0
    # carpoolers = userqueries.get_carpool_closeby_filter(session['username'],0,0,25,0)
    # user_geo = crud.get_user_by_email(session['username']).address_geo
    # for carpooler in carpoolers:
    #     carpooler.address_longitude = userqueries.distance_between_addresses(user_geo,carpooler.address_geo)
    #     carpooler.latitude = carpooler.car[0].seats
        
    # return render_template('search.html', carpoolers = carpoolers)


""" Display carpoolers with filter to whom you can send request"""
@app.route('/search_filter_carpool' , methods=['POST'])
def search_carpool_filter():
    """ List all carpoolers available with smoking, pet and distance filter"""
    session['smoking_preference'] = 0
    session['pets_preference'] = 0
    
    smoking = 0
    pets = 0
    

    if (request.form.get('search_smoking') == 'YES'):
        smoking = 1
        session['smoking_preference'] = 1
    
    if (request.form.get('search_pets') == 'YES'):
        pets = 1
        session['pets_preference'] = 1
    
    distance = request.form.get('distance')
    if distance == "ANY":
        distance = 25
    else:
        distance = float(distance)

    grade = request.form.get('grade')
    if grade == "ANY":
        grade = 0
    else:
        grade = int(grade)

    session['grade'] = grade
    session['distance'] = distance

    user_geo = crud.get_user_by_email(session['username']).address_geo
    carpoolers = userqueries.get_carpool_closeby_filter(session['username'],smoking,pets,distance,grade)
    for carpooler in carpoolers:
        carpooler.address_longitude = userqueries.distance_between_addresses(user_geo,carpooler.address_geo)
        carpooler.latitude = carpooler.car[0].seats


    return render_template('search.html', carpoolers = carpoolers)


""" Return JSON of carpoolers nearby """
@app.route("/search_carpoolers/json")
def search_carpoolers_info():
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
        for carpooler in  userqueries.get_carpool_closeby_filter(session['username'],session['smoking_preference'],session['pets_preference'],session['distance'],session['grade'])
    ]

    return jsonify(carpoolers)


""" Choose a carpooler to send request to"""
@app.route('/send_carpool_request', methods =['POST'])
def display_individual_user():
    """ Choose the carpooler to whom the user is sending the request """
    request_user_id=request.form.get('carpoolrequest')
    request_user = crud.get_user_by_id(request_user_id)
    session['send_request_phone'] = request_user.phone_number
    request_user_children = request_user.children
    login_user = crud.get_user_by_email(session['username'])
    session['send_request_to'] = request_user_id
    session['requesting_phone_number'] = request_user.phone_number
    return render_template('send_request.html', request_user = request_user, request_user_children = request_user_children,login_user=login_user  )


""" Send a request through the web app and twilio SMS"""
@app.route('/send_request_phone', methods=['POST'])
def send_request():
    """ Send a carpool request to a carpooler through app and twilio"""
    notes = request.form.get('request_note').strip()

    login_user = crud.get_user_by_email(session['username'])
    from_user = login_user.user_id
    to_user = session['send_request_to']
    child_id = login_user.children[0].child_id
    request_note = notes
    request_datetime = datetime.now() 
    crud.create_request(from_user,to_user,child_id,request_note,"","S",request_datetime)
    # send_message.send_message(session['send_request_phone'],request_note)
    carpoolers = userqueries.get_carpool_closeby_filter(session['username'],0,0,25,0)
    user_geo = crud.get_user_by_email(session['username']).address_geo
    for carpooler in carpoolers:
        carpooler.address_longitude = userqueries.distance_between_addresses(user_geo,carpooler.address_geo)
        carpooler.latitude = carpooler.car[0].seats
    flash (f"Request message sent to {session['requesting_phone_number']} ")
    return render_template('search.html', carpoolers = carpoolers)
    

""" Return JSON of the login user and the user to whom request is sent """
@app.route("/request_peson/json")
def request_person_info():
    request_user = crud.get_user_by_id(session['send_request_to'])
    login_user = crud.get_user_by_email(session['username'])
    # a = session['send_request_to']
    # b = session['username']
    # print (f'send_to {a} and user in {b}')
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


@app.route('/back_requests_page')
def show_requests_page():
    carpoolers = show_requests_details()
    return render_template('requests.html', carpoolers = carpoolers)

""" Display all carpoolers who have sent you a request to carpool"""
@app.route('/accept_deny_request', methods=['POST'])
def show_requests():
    """ Display all carpoolers who have sent you a request to carpool"""
    carpoolers = show_requests_details()
    # carpoolers = userqueries.get_requests_recieved(session['username'])
    # user_geo = crud.get_user_by_email(session['username']).address_geo
    # for carpooler in carpoolers:
    #     carpooler.address_longitude = userqueries.distance_between_addresses(user_geo,carpooler.address_geo)
    return render_template('requests.html', carpoolers = carpoolers)


def show_requests_details():
    carpoolers = userqueries.get_requests_recieved(session['username'])
    user_geo = crud.get_user_by_email(session['username']).address_geo
    for carpooler in carpoolers:
        carpooler.address_longitude = userqueries.distance_between_addresses(user_geo,carpooler.address_geo)
    return carpoolers

""" Choose a carpooler to whom the user will respond to"""
@app.route('/individual_accept_deny', methods= ['POST'])
def accept_deny_request():
    """ Choose a carpooler to whom the user will respond to"""
    request_user_id=request.form.get('carpoolrequest')
    request_user = crud.get_user_by_id(request_user_id)
    session['send_decision_phone'] = request_user.phone_number
    request_user_children = request_user.children
    login_user = crud.get_user_by_email( session['username'])
    session['accept_deny_userid'] = request_user_id
    additional_message = userqueries.get_additional_message(session['user_id'],request_user.user_id)
    return render_template('accept_deny.html', request_user = request_user, request_user_children = request_user_children,login_user=login_user,additional_message=additional_message,message_len=len(additional_message))


""" Return JSON of the login user and the user whose request is viewed"""
@app.route("/accept_deny_peson/json")
def accept_deny_person_info():
    request_user = crud.get_user_by_id(session['accept_deny_userid'])
    login_user = crud.get_user_by_email(session['username'])
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
            "phone": "1222424",
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
            "phone": "123433",
        }
    ]

    return jsonify(carpoolers)



@app.route('/accept_deny_individual', methods= ['POST'])
def accept_deny_individual_request():
    accept_or_deny = request.form.get('send_request')
    if (accept_or_deny == "Accept"):
        request_code = "A"
    else:
        request_code = "D"

    notes = request.form.get('decission_note')

    login_user = crud.get_user_by_email(session['username'])
    from_user = login_user.user_id
    to_user = session['accept_deny_userid']
    child_id = login_user.children[0].child_id
    request_note = notes
    request_datetime = datetime.now() 
    crud.create_request(from_user,to_user,child_id,request_note,"",request_code,request_datetime)
    send_message.send_message(session['send_decision_phone'],request_note)
    flash (f"Request message sent to {session['requesting_phone_number']} ")
    if request_code == "A":
        userqueries.respond_denial_to_others(from_user,to_user)
        buddies = userqueries.get_user_buddies(session['username'])
        buddy = crud.get_user_by_id(buddies[0].user_id)
        session['buddy_phone']= buddy.phone_number
        session['buddy_id'] = buddy.user_id
        request_user_children = buddy.children
        return render_template('user.html',buddies=buddies,number = len(buddies),request_user_children=request_user_children)
    return redirect('/') 

   







@app.route('/search_carpool',methods=['POST'])
def user_carpoolers():
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
        for carpooler in  userqueries.get_carpool_closeby_filter(session['username'],0,0)
    ]

    return jsonify(carpoolers)


@app.route('/logout') 
def logout():  
    return render_template('logout.html')

# 2,4,2,from 2 to 4,,S,2020-10-22 09:21:21
# 2,6,9,from 2 to 6,,S,2020-10-22 11:21:21
# 1,2,1,from 1 to 2,2 accepted,A,2020-10-24 17:37:21
# 2,4,2,from 2 to 4,4 denied,D,2020-10-23 09:21:21
# 2,6,9,from 2 to 6,6 accepted,A,2020-10-23 11:51:21

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)