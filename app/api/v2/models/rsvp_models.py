""" Manages all the meetup functions """
from datetime import date
import json
import jwt
from flask import Flask, request, jsonify
from app.api.v2.utils.user_validator import UsersHelper
from app.api.v2.utils.database_helper import DatabaseHelper
from app.api.v2.models.users_model import UsersModel

database = DatabaseHelper()


class RsvpModel():

    def __init__(self):
        ''' Initializes a response from user '''
        self.helpers = UsersHelper()

    def rsvp_meetup(self, meetup_id, request):
        ''' Allows a user to rsvp a meetup '''
        rsvp = {}
        keys_expected = ["response"]

        result = self.helpers.is_valid_user_request(keys_expected, request)

        if result[0] == 0:
            return result[1], 400

        result = self.helpers.is_blank_field(request)

        if result[0] == 0:
            return result[1], 400
        data = request.get_json()
        token = request.headers.get('Authorization').split()[1]
        user_id = jwt.decode(token, 'Felix45', algorithms=['HS256'])
        expression = "meetup_id=%d AND user_id=%d" %(meetup_id, user_id['user'])
        if database.find_in_db('rsvps',expression):
            return jsonify({'msg':'This rsvp already exists', 'status': 409}), 409
        columns = 'meetup_id,user_id,response'
        values  = "%d, %d , '%s'" % (user_id['user'], meetup_id, data['response'])

        if not database.find_in_db('users', 'id=%d' % (user_id['user'],)):
            return jsonify({"error": "User does not exist on questioner", "status": 404}), 404
        if not database.find_in_db('meetups', 'Id=%d'%(meetup_id)):
            return jsonify({"error": "Meetup does not exist on questioner", "status": 404}), 404
        
        return database.insert_into_db('rsvps', columns, values, 'rsvp')
