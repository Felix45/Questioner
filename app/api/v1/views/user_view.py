from flask import Blueprint, Flask , jsonify , request 

from app.api.v1.models.users_model import UsersModel

userV1 = Blueprint('user_v1',__name__,url_prefix='/api/v1')

users_model = UsersModel()

@userV1.route('/users/list/', methods=['GET'])
def get_users():
	return users_model.get_users()
	
@userV1.route('/users/add/', methods=['POST'])
def add_user():
	return users_model.add_user(request)