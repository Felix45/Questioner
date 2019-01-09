""" Manages users details """
import datetime
from flask import Flask, jsonify, request

users = []

class UsersModel:

    def add_user(self,user_request):
        """ register a user """

        new_user = {}

        user_id    = len(users)+1
        first_name = user_request.get_json()['firstname']
        lastname   = user_request.get_json()['lastname']
        othername  = user_request.get_json()['othername']
        username   = user_request.get_json()['username']
        email      = user_request.get_json()['email']
        isAdmin    = user_request.get_json()['isAdmin']
        password   = user_request.get_json()['password']
        cpassword  = user_request.get_json()['cpassword']
        phoneNumber= user_request.get_json()['phonerNumber']



        new_user['user_id']   = user_id
        new_user['firstname'] = first_name
        new_user['lastname']  = lastname
        new_user['othername'] = othername
        new_user['username']  = username
        new_user['email']     = email
        new_user['password']  = password
        new_user['registered'] = ""
        new_user['isAdmin']    = isAdmin
        new_user['phoneNumber']    = phoneNumber

        users.append(new_user)

        return jsonify({'msg':'user added successfully'}) , 200

