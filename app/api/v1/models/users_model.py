""" Manages users details """
from datetime import date
from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from app.api.v1.utils.user_validator import UsersHelper


users = []
helpers = UsersHelper()


class UsersModel:

    def add_user(self, user_request):
        """ register a user """
        keys_expected = ['firstname', 'lastname', 'othername', 'username', 'email', 'isAdmin', 'password', 'cpassword', 'phoneNumber']
        
        ret = helpers.is_valid_user_request(keys_expected, user_request)

        if ret[0] == 0:
            return ret[1], 400

        ret = helpers.is_blank_field(user_request)

        if ret[0] == 0:
            return ret[1], 400

        ret = helpers.is_available(user_request.get_json()['email'], 'email',
                                   users, user_id=0)
        if ret[0] == 0:
            return ret[1], 409

        ret = helpers.is_available(user_request.get_json()['username'],
                                   'username', users, user_id=0)
        if ret[0] == 0:
            return ret[1], 409

        validator = helpers.is_valid_email(user_request.get_json()['email'])  
        if not validator[0]:
            return validator[1], 400

        ret = helpers.is_valid_password(user_request.get_json()['password'],
                                        user_request.get_json()['cpassword'])
        if ret[0] == 0:
            return ret[1], 400

        self.insert_db(user_request)     
        return jsonify({'msg': 'user added successfully'}), 200

    def insert_db(self, user_request):
        new_user = {}
        password = user_request.get_json()['password']
        new_user['user_id'] = len(users)+1
        new_user['firstname'] = user_request.get_json()['firstname']
        new_user['lastname'] = user_request.get_json()['lastname']
        new_user['othername'] = user_request.get_json()['othername']
        new_user['username'] = user_request.get_json()['username']
        new_user['email'] = user_request.get_json()['email']
        new_user['password'] = generate_password_hash(password)
        new_user['registered'] = date.today()
        new_user['isAdmin'] = user_request.get_json()['isAdmin']
        new_user['phoneNumber'] = user_request.get_json()['phoneNumber']

        users.append(new_user)

    def get_users(self):
        """ A list containing all users """
        global users

        if len(users) == 0:
            return jsonify({'msg': 'no user was found'})    
        return jsonify({"data": users}), 200

    def login_user(self, request):
        global users
        keys_expected = ['username', 'password']

        validator = helpers.is_valid_user_request(keys_expected, request)

        if not validator[0]:
            return validator[1], 400

        validator = helpers.is_blank_field(request)

        if not validator[0]:
            return validator[1], 400

        username = request.get_json()['username']
        password = request.get_json()['password']

        logged_in = [u for u in users if u['username'] == username and 
                     check_password_hash(u['password'], password)]

        if len(logged_in) > 0:
            return jsonify({'msg': 'logged in', "data": logged_in}), 200
        return jsonify({'msg': 'user {} not found:'.format(username)}), 404