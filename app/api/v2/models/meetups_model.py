""" Manages all the meetup functions """
from datetime import date
import json
from flask import Flask, request, jsonify
from app.api.v2.utils.user_validator import UsersHelper
from app.api.v2.utils.database_helper import DatabaseHelper
from app.api.v2.models.users_model import UsersModel

database = DatabaseHelper()


class MeetUpsModel():

    def __init__(self):
        self.meetups = []
        self.questions = []
        self.rsvps = []
        self.helpers = UsersHelper()

    def add_meetup(self, user_request):
        meetup = user_request.get_json()

        keys_expected = ["location", "images", "topic", "happeningOn", "Tags"]

        result = self.helpers.is_valid_user_request(keys_expected, user_request)

        if result[0] == 0:
            return result[1], 400

        result = self.helpers.is_blank_field(user_request)

        if result[0] == 0:
            return result[1], 400

        columns = 'user_id, location, images, topic, happeningOn, Tags, created_on'
        values= "1"+",'"+meetup['location']+"','"+",".join(meetup['images'])+"','"+meetup["topic"]+"','"+meetup['happeningOn']+"','"+",".join(meetup['Tags'])+"','"\
                +str(date.today())+"'"

        return database.insert_into_db('meetups', columns, values, 'Meetup')
    
    def get_meetups(self):
        expression = "happeningon >= '{0}'".format(date.today())
        self.meetups = database.find_in_db('meetups', expression)
        if self.meetups:
            return jsonify({"msg": "Meetups were found", "data": self.meetups, "status": 200})
        return jsonify({"msg": "Meetups were not found", "data": self.meetups, "status": 404})

    def get_a_meetup(self, search_id):
        """ Returns a specific meetup record """
        expression = "id={0}".format(search_id)
        meetup = database.find_in_db('meetups', expression)
        
        if meetup:
            return jsonify({"msg": "Meetup was found", "data": meetup, "status": 200})   
        return jsonify({"msg": "Meetup was not found", "data": [], "status": 404}), 404
    
    def delete_meetup(self, meetup_id):
        expression = "id={0}".format(meetup_id)
        meetup = database.find_in_db('meetups', expression)

        if meetup:
            database.delete_record("meetups", "id", meetup_id)
            return jsonify({"msg": "meetup was deleted", "status": 200 }), 200 
        return jsonify({"msg": "meetup was not found", "status": 404}), 404

    def rsvp_meetup(self, meetup_id, request):
        ''' Allows a user to rsvp a meetup '''
        rsvp = {}
        keys_expected = ["user", "meetup", "response"]

        result = self.helpers.is_valid_user_request(keys_expected, request)

        if result[0] == 0:
            return result[1], 400

        result = self.helpers.is_blank_field(request)

        if result[0] == 0:
            return result[1], 400

        meetup = [item for item in self.meetups if item["id"] == meetup_id]

        if meetup:
            rsvp["id"] = len(self.rsvps) + 1
            rsvp["meetup"] = meetup_id
            rsvp["user"] = request.get_json()["user"]
            rsvp["response"] = request.get_json()["response"]
            self.rsvps.append(rsvp)
            return jsonify({"msg": "rsvp was created", "data": rsvp, "status": 201}), 201

        return jsonify({"msg": "Meetup was not found", "status": 404}), 404
