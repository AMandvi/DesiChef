from flask_app import CLIENT_ID, app
from flask import Flask, render_template, request, redirect, session
from flask_app.helpers.user_helper import getLoggedUser
from flask_app.models.meal_model import Meal
from flask_app.models.order_model import Order         
from flask_app.models.user_model import User
from flask import flash
from datetime import datetime, timedelta


@app.route('/myorders')
def myorders():
    logged_user = getLoggedUser()
    data = {
        'id': logged_user.id
    }
    order_meals = Order.get_meals_for_user(data)

    now = datetime.now()
    monday = now - timedelta(days = now.weekday())
    date = monday.date()
    date_string = "Orders for week of " + str(date.month) + "/" + str(date.day)
    print(date_string)
    return render_template("myorders.html", order_meals=order_meals, logged_user=logged_user, date = date_string)