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
    
    if existing_user == None:
        flash("User not found. Create an account")
    else:
        flash ("Logged in")

    return redirect('/') 


@app.route('/new_user', methods=['POST'])
def new_user():
    """ User Registration Page """
    return render_template('newuser.html')

if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)