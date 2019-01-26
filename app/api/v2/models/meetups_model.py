""" Manages all the meetup functions """
from datetime import date
import json
import jwt
import re
from flask import Flask, request, jsonify
from app.api.v2.utils.user_validator import UsersHelper
from app.api.v2.utils.database_helper import DatabaseHelper
from app.api.v2.models.users_model import UsersModel

database = DatabaseHelper()
usermodel = UsersModel()


class MeetUpsModel():

    def __init__(self):
        self.meetups = []
        self.questions = []
        self.rsvps = []
        self.helpers = UsersHelper()

    def add_meetup(self, user_request):
        meetup = user_request.get_json()

        keys_expected = ["location", "images", "topic", "happeningOn", "Tags"]

        result = self.helpers.is_valid_user_request(keys_expected,
                                                    user_request)

        if result[0] == 0:
            return result[1], 400

        result = self.helpers.is_blank_field(user_request)

        if result[0] == 0:
            return result[1], 400
        token = request.headers.get('Authorization').split()[1]
        user_id = jwt.decode(token, 'Felix45', algorithms=['HS256'])
   
        if not UsersModel().get_admin_user(user_id):
            return jsonify({'msg': 'You can not add a meetup, only admin', 'status': 403}), 403

        columns = 'user_id, location, images, topic, happeningOn, Tags,\
                   created_on'
        
        images = self.construct_list(meetup['images'])
        tags = self.construct_list(meetup['Tags'])
        
        values = "%d,'%s','%s','%s','%s','%s','%s'" % (user_id['user'],
                  meetup['location'],
                  images, meetup["topic"], meetup['happeningOn'], tags,
                  str(date.today()))
        
        return database.insert_into_db('meetups', columns, values, 'Meetup')
    
    def get_meetups(self):
        expression = "happeningon >= '{0}'".format(date.today())
        self.meetups = database.find_in_db('meetups', expression)
        if self.meetups:
            for meetup in self.meetups:
                meetup['tags'] = self.construct_list(meetup['tags'], True)
                meetup['images'] = self.construct_list(meetup['images'], True)
            return jsonify({"msg": "Meetups were found", "data": self.meetups, "status": 200})
        return jsonify({"msg": "Meetups were not found", "data": self.meetups, "status": 404})

    def get_a_meetup(self, search_id):
        """ Returns a specific meetup record """
        expression = "id={0}".format(search_id)
        meetup = database.find_in_db('meetups', expression)
        
        if meetup:
            meetup[0]['tags'] = self.construct_list(meetup[0]['tags'],
                                                    fetch_items=True)
            meetup[0]['images'] = self.construct_list(meetup[0]['images'],
                                                      fetch_items=True)
            return jsonify({"msg": "Meetup was found", "data": meetup, "status": 200})   
        return jsonify({"msg": "Meetup was not found", "data": [], "status": 404}), 404
    
    def delete_meetup(self, meetup_id):
        token = request.headers.get('Authorization').split()[1]
        user_id = jwt.decode(token, 'Felix45', algorithms=['HS256'])
        if not UsersModel().get_admin_user(user_id):
            return jsonify({'msg': 'You can not delete a meetup, only admin can', 'status': 403}), 403
        
        expression = "id={0}".format(meetup_id)
        meetup = database.find_in_db('meetups', expression)
        
        if meetup:
            database.delete_record("meetups", "id", meetup_id)
            return jsonify({"msg": "meetup was deleted", "status": 200,
                            'data': meetup}), 200 
        return jsonify({"msg": "meetup was not found", "status": 404, "data": 
                        meetup}), 404

    def construct_list(self, item, fetch_items=False):
        ''' Ensures items are stored in lists '''
        if type(item) is list:
            return ','.join(item)
        elif fetch_items:
            return item.split(',')
        return str(item)
