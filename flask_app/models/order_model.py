from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

from flask_app.models.meal_model import Meal

class Order:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.user_id = data['user_id']
        self.meal_id = data['meal_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    def create(data):
        query = """
                INSERT INTO orders (user_id, meal_id)
                VALUES (%(user_id)s, %(meal_id)s);
            """
        return connectToMySQL(DATABASE).query_db(query,data) 

    def get_meals_for_user(data):
        query = """ 
                SELECT * FROM orders LEFT JOIN meals ON orders.meal_id = meals.id
                WHERE orders.user_id = %(id)s;
            """
        results = connectToMySQL(DATABASE).query_db(query,data)
        all_meals = [] 
        if results:
            for row in results:
                meal_data = {
                    **row,
                    'id' : row['meals.id'],
                    'created_at' : row['meals.created_at'],
                    'updated_at' : row['meals.updated_at']
                }
                this_meal = Meal(meal_data)
                all_meals.append(this_meal)
            return all_meals
        else : 
            return []
