"""Server for movie ratings app."""
from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View Homepage"""
    
    return render_template('homepage.html')
    
@app.route('/login', methods=['POST'])   
def user_login():
    """ Validate Login"""
    # if (request.form.get('action') == 'Login'):
    email = request.form.get('username')
    password = request.form.get('password')
    existing_user = crud.get_user_by_email(email)
    
    if (existing_user == None):
        flash("User not found. Create an account")
    elif (crud.check_login_details(email,password) == False):
        flash ("Invalid Password")
    else:
        flash ("Login Successful")

    return redirect('/') 


@app.route('/new_user', methods=['POST'])
def new_user():
    """ User Registration Page """
    return render_template('newuser.html')

@app.route('/create_user', methods=['POST'])
def create_user():
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
    
    return redirect('/') 

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)