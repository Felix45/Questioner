""" Manages users details """
from datetime import date
from flask import Flask, jsonify, request
from app.api.v1.utils.user_validator import UsersHelper

users = []
helpers = UsersHelper()

class UsersModel:

    def add_user(self,user_request):
        """ register a user """
        keys_expected = ['firstname','lastname','othername','username','email','isAdmin','password','cpassword','phoneNumber']
        new_user = {}

        ret = helpers.is_valid_user_request(keys_expected,user_request)

        if ret[0] == 0:
            return ret[1]  , 400


        ret = helpers.is_blank_field(user_request)

        if ret[0] == 0:
            return ret[1] , 400


        user_id    = len(users)+1
        first_name = user_request.get_json()['firstname']
        lastname   = user_request.get_json()['lastname']
        othername  = user_request.get_json()['othername']
        username   = user_request.get_json()['username']
        email      = user_request.get_json()['email']
        isAdmin    = user_request.get_json()['isAdmin']
        password   = user_request.get_json()['password']
        cpassword  = user_request.get_json()['cpassword']
        phoneNumber= user_request.get_json()['phoneNumber']

       

        ret = helpers.is_available(email , 'email', users , user_id=0)
        if ret[0] == 0:
            return ret[1] , 409

        ret = helpers.is_available(username , 'username', users , user_id=0)
        if ret[0] == 0:
            return ret[1] , 409

        validator = helpers.is_valid_email(email)
        
			
        if not validator[0]:
			return validator[1] , 400

        ret = helpers.is_valid_password(password,cpassword)
        if ret[0] == 0:
            return ret[1] , 400



        new_user['user_id']   = user_id
        new_user['firstname'] = first_name
        new_user['lastname']  = lastname
        new_user['othername'] = othername
        new_user['username']  = username
        new_user['email']     = email
        new_user['password']  = password
        new_user['registered'] = date.today()
        new_user['isAdmin']    = isAdmin
        new_user['phoneNumber']    = phoneNumber

        users.append(new_user)

        return jsonify({'msg':'user added successfully'}) , 200

    def get_users(self):
        """ A list containing all users """
        global users

        if len(users) == 0:
            return jsonify({'msg':'no user was found'})
        
        return jsonify({"data":users}) , 200


