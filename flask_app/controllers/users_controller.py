from flask_app import CLIENT_ID, app
from flask import Flask, render_template, request, redirect, session
from flask_app.helpers.user_helper import getLoggedUser
from flask_app.models.meal_model import Meal         
from flask_bcrypt import Bcrypt
from flask_app.models.user_model import User
from flask import flash
from google.oauth2 import id_token
from google.auth.transport import requests

bcrypt = Bcrypt(app)

@app.route('/login')
def index():
    return render_template("index.html")

@app.route('/register')
def signup():
    return render_template("signup.html")

@app.route('/users/register/gmail',methods = ['POST'])
def register_gmail_user():
    google_token = request.form['credential']
    idInfo = id_token.verify_oauth2_token(google_token, requests.Request(), CLIENT_ID)
    data = {
        **idInfo,
        'first_name': idInfo['given_name'],
        'last_name': idInfo['family_name'],
        'password': None
    }
    user_id = User.create(data)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/users/register', methods = ['POST'])        #registeration form
def reg_user():
    if not User.validator(request.form):
        return redirect('/register')
        #if not valid send back to register
    #hashing the pass
    hashed_pass = bcrypt.generate_password_hash(request.form['password'])
    data =  {
        **request.form,
        'password': hashed_pass,
        'conf_pass': hashed_pass      #this is unnecessary but makes us feel safe
    }
    #creating account with hashed pass
    logged_user_id = User.create(data)
    #storing the user id insession to consider them logged in
    session['user_id'] =  logged_user_id
    return redirect('/dashboard')


@app.route('/users/login/gmail',methods = ['POST'])
def login_gmail_user():
    google_token = request.form['credential']
    idInfo = id_token.verify_oauth2_token(google_token, requests.Request(), CLIENT_ID)
    data = {
        **idInfo,
    }
    user = User.get_by_email(data)
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/users/login',methods = ['POST'])            #login form
def log_user():
    data = {
        'email': request.form['email']
    }
    user_in_db = User.get_by_email(request.form)
    if not user_in_db:
        flash("Invalid credentials", "log")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password,request.form['password']):
        flash("Invalid credentials", "log")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')

@app.route('/users/logout')                       #get request
def log_out():
    #deleting user_id from session logs user out
    del session['user_id']
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    logged_user = getLoggedUser()
    week_meals = Meal.get_all_meals_for_week()
    return render_template("welcome.html", week_meals = week_meals, logged_user=logged_user)

@app.route('/admin')
def admin():
    return render_template("admin.html")

@app.route('/meal/create', methods = ['POST'])
def create_meal():
    data =  {
        **request.form,
        'is_vegan': 1 if 'is_vegan' in request.form else 0,
        'is_diet': 1 if 'is_diet' in request.form else 0
    }
    Meal.create(data)
    return redirect("/dashboard")