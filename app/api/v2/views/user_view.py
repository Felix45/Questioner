from flask import Blueprint, Flask, jsonify, request

from app.api.v2.models.users_model import UsersModel

userV2 = Blueprint('user_v2', __name__, url_prefix='/api/v2')

users_model = UsersModel()


@userV2.route('/users/list/', methods=['GET'])
@users_model.token_required
def get_users():
	return users_model.get_users()


@userV2.route('/users/add/', methods=['POST'])
def add_user():
	return users_model.add_user(request)

@userV2.route('/auth/login/', methods=['POST'])
def login_user():
	return users_model.login_user(request)

@userV2.route('/auth/update/', methods=['POST'])
@users_model.token_required
def update_user():
	return users_model.update_user(request)
