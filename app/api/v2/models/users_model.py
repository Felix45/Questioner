""" Manages users details """
import jwt
import re
import string
import datetime
from datetime import date
from functools import wraps

from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from app.api.v2.utils.user_validator import UsersHelper
from app.api.v2.utils.database_helper import DatabaseHelper


users = []
token = ''
helpers = UsersHelper()
database = DatabaseHelper()


class UsersModel:

    def add_user(self, user_request):
        """ register a user """
        global users, database
        keys_expected = ['firstname', 'lastname', 'othername', 'username',
                         'email', 'isAdmin', 'password', 'cpassword',
                         'phoneNumber']
 
        ret = helpers.is_valid_user_request(keys_expected, user_request)

        if ret[0] == 0:
            return ret[1], 400

        ret = helpers.is_blank_field(user_request)

        if ret[0] == 0:
            return ret[1], 400

        expression = 'email='+"'"+user_request.get_json()['email']+"'"
        users = database.find_in_db('users', expression)
        print(expression)
        if users:
            return jsonify({'message': 'email is already in use '}), 409
        
        expression = 'username='+"'"+user_request.get_json()['username']+"'"
        users = database.find_in_db('users', expression)

        if users:
            return jsonify({'message': 'username is already in use '}), 409

        validator = helpers.is_valid_email(user_request.get_json()['email'])  
        if not validator[0]:
            return validator[1], 400

        ret = helpers.is_valid_password(user_request.get_json()['password'],
                                        user_request.get_json()['cpassword'])
        if ret[0] == 0:
            return ret[1], 400
  
        return self.insert_db(user_request)

    def insert_db(self, user_request):
        ''' Adds a user into the datbase '''
        new_user = {}
        password = user_request.get_json()['password']
        new_user['firstname'] = user_request.get_json()['firstname']
        new_user['lastname'] = user_request.get_json()['lastname']
        new_user['othername'] = user_request.get_json()['othername']
        new_user['username'] = user_request.get_json()['username']
        new_user['email'] = user_request.get_json()['email']
        new_user['password'] = generate_password_hash(password)
        new_user['registered'] = str(date.today())
        new_user['isadmin'] = user_request.get_json()['isAdmin']
        new_user['phone_number'] = user_request.get_json()['phoneNumber']

        if not re.match(r'[0-9]', new_user['phone_number']):
            return jsonify({'msg': 'Phone number is not correct', 'status': 400}), 400

        columns = 'firstname, lastname, othername, username, email, password, \
                   registered, isadmin, phone_number'
        values = "'"+new_user['firstname']+"','"+new_user['lastname']+"', \
                '"+new_user['othername']+"','"+new_user['username']+"', \
                '"+new_user['email']+"','" + new_user['password']+"', \
                '"+new_user['registered']+"',"+new_user['isadmin']+", \
                '"+new_user['phone_number']+"'"
        
        return database.insert_into_db('users', columns, values, 'user')
        
    def get_users(self):
        """ A list containing all users """
        users = database.fethall_records('users')

        if len(users) == 0:
            return jsonify({'msg': 'no user was found', 'data': users}), 404    
        return jsonify({"data": users}), 200
    
    def token_required(self, f):
        ''' Check if a user has a valid token '''
        @wraps(f)
        def decorated(*args, **kwargs):
            if not request.headers.get('Authorization'):
                return jsonify({'msg': 'You need a login token to view this'})
            try:
                token = request.headers.get('Authorization').split()[1]
                data = jwt.decode(token, 'Felix45', algorithms=["HS256"])
            except:
                return jsonify({'msg': 'You need to login to view this'}), 403

            return f(*args, **kwargs)
        return decorated

    def login_user(self, request):
        ''' Login a user in to the application '''
        global users, token
        keys_expected = ['username', 'password']

        validator = helpers.is_valid_user_request(keys_expected, request)

        if not validator[0]:
            return validator[1], 400

        validator = helpers.is_blank_field(request)

        if not validator[0]:
            return validator[1], 400

        username = request.get_json()['username']
        password = request.get_json()['password']

        expression = 'username='+"'"+username+"'"
        users = database.find_in_db('users', expression)
        
        if users and check_password_hash(users[0]['password'], password):
            token = jwt.encode({"user": users[0]['id'],
                                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                                }, 'Felix45', algorithm='HS256').decode('UTF-8')
            return jsonify({'msg': 'logged in', "data": users, "token":
                            token, "status": 200}), 200
        return jsonify({'msg': 'user {} not found:'.format(username), "status":
                        404}), 404

    def get_logged_in_user(self, user_id):
        ''' Returns details of logged in user '''
        
        expression = "isadmin='%s' AND id=%d" % (str(True).lower(), user_id['user'])
        user = database.find_in_db('users', expression)

        return user
