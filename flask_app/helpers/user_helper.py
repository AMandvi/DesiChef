from flask import session
from flask_app.models.user_model import User

def getLoggedUser():
    logged_user = None
    if 'user_id' in session:
        data={
            'id':session['user_id']
        }
        logged_user = User.get_by_id(data)
    return logged_user