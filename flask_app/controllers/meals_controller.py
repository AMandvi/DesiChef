from flask_app import app
from flask import Flask, render_template, request, redirect, session
from flask_app.helpers.user_helper import getLoggedUser
from flask_app.models.meal_model import Meal
from flask_app.models.order_model import Order         
from flask_bcrypt import Bcrypt
from flask_app.models.user_model import User
from flask import flash
from flask import jsonify

ONE_MEAL_PRICE = 12

@app.route('/weeklymenu')
def weeklymenu():
    logged_user = getLoggedUser()
    week_meals = Meal.get_all_meals_for_week()
    return render_template("weeklymenu.html", week_meals=week_meals, logged_user=logged_user)

@app.route('/meal/select', methods = ['POST'])
def select_meals():
    meals = request.form.getlist('meal_checkbox')
    session['meals'] = meals
    return redirect('/meal/payment')

@app.route('/meal/payment')
def meal_payment():
    price = ONE_MEAL_PRICE * len(session['meals'])
    num_meal = str(len(session['meals']))
    meal_price_str = str(price)
    return render_template("payment.html", meal_price = price, num_meal = num_meal, meal_price_str=meal_price_str)

@app.route('/meal/save', methods = ['POST'])
def save_meal():
    print (session['meals'])
    meal_ids = session['meals']
    user_id = session['user_id']

    for meal in meal_ids:
        data = {
            'meal_id': meal,
            'user_id': user_id
        }
        Order.create(data)

    return jsonify()

@app.route('/meals/<int:id>/view')
def view_meal(id):
    data = {
        'id': id
    }
    this_meal = Meal.get_one(data)
    return render_template('mealrecipe.html', this_meal = this_meal)