from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import datetime

class Meal:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.recipe = data['recipe']
        self.date_available = data['date_available']
        self.is_vegan = data['is_vegan']
        self.is_diet = data['is_diet']
        self.image_link = data['image_link']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def create(cls,data:dict) -> int:
        query = "INSERT INTO meals (name, description, recipe, date_available, is_vegan, is_diet, image_link) VALUES (%(name)s, %(description)s, %(recipe)s, %(date_available)s, %(is_vegan)s, %(is_diet)s, %(image_link)s)"
        meal_id = connectToMySQL(DATABASE).query_db(query,data)
        return meal_id
    
    @classmethod
    def get_all_meals_for_week(cls) -> list:
        query = "SELECT * FROM meals;"
        results =  connectToMySQL(DATABASE).query_db(query)
        all_meals = [] 
        if results:
            for values in results:
                this_meal = cls(values)
                all_meals.append(this_meal)
            return all_meals
        else : 
            return []
    
    @classmethod
    def get_one(cls,data):
        query = """
        SELECT * FROM meals WHERE id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            row = results[0]
            this_meal = cls(row)
            return this_meal
        return None