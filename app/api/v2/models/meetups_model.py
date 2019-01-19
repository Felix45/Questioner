""" Manages all the meetup functions """
from datetime import date
import json
from flask import Flask, request, jsonify
from app.api.v1.utils.user_validator import UsersHelper
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

        ret = self.helpers.is_valid_user_request(keys_expected, user_request)

        if ret[0] == 0:
            return ret[1], 400

        ret = self.helpers.is_blank_field(user_request)

        if ret[0] == 0:
            return ret[1], 400

        columns = 'user_id, location, images, topic, happeningOn, Tags, created_on'
        values= "1"+",'"+meetup['location']+"','"+",".join(meetup['images'])+"','"+meetup["topic"]+"','"+meetup['happeningOn']+"','"+",".join(meetup['Tags'])+"','"\
                +str(date.today())+"'"

        return database.insert_into_db('meetups', columns, values, 'Meetup')

        #return jsonify({"msg": "meetup was added", "data": meetups, "status": 200})

    def get_meetups(self):
        if len(self.meetups) == 0:
            return jsonify({"msg": "no users were found", "data": self.meetups, "status": 200})
        return jsonify({"msg": "users", "data": self.meetups, "status": 200})

    def get_a_meetup(self, search_id):
        """ Returns a specific meetup record """

        if len(self.meetups) == 0:
            return jsonify({"msg": "no users were found", "data": self.meetups, "status": 200}), 200      
        for meetup in self.meetups:
            if meetup['id'] == search_id:
                return jsonify({"msg": "user was found", "data": meetup, "status": 200})     
        return jsonify({"msg": "user was not found", "data": [], "status": 404}), 404

    def delete_meetup(self, meetup_id):
        expression = "id={0}".format(meetup_id)
        meetup = database.find_in_db('meetups',expression)

        if meetup:
            database.delete_record("meetups", "id",meetup_id)
            return jsonify({"msg":"meetup was deleted", "status":200 }), 200 
        return jsonify({"msg":"meetup was not found", "status": 404}), 404

    def add_a_question(self, user_request):
        """ Add a question record """
        question = {}
        keys_expected = ["user", "meetup", "title", "body"]

        ret = self.helpers.is_valid_user_request(keys_expected, user_request)

        if ret[0] == 0:
            return ret[1], 400

        ret = self.helpers.is_blank_field(user_request)

        if ret[0] == 0:
            return ret[1], 400
        question['id'] = len(self.questions) + 1
        question['votes'] = 0
        question['user'] = user_request.get_json()['user']
        question['meetup'] = user_request.get_json()['meetup']
        question['title'] = user_request.get_json()['title']
        question['body'] = user_request.get_json()['body']

        self.questions.append(question)
        return jsonify({"msg": "question was added", "status": 201}), 201

    def vote(self, vote, question_id, type):
        """ Allows a user to upvote or downvote a question """

        question = [q for q in self.questions if q["id"] == question_id]
      
        if question:
            question[0]["votes"] = int(question[0]["votes"]) + int(vote)
            question[0]["votes"] = 0 if question[0]["votes"] < 0 else question[0]["votes"]
            return jsonify({"msg": "{} was successful".format(type),
                            "status": 201, "data": self.questions}), 201

        return jsonify({"msg": "Question was not found", "status": 404}), 404  

    def rsvp_meetup(self, meetup_id, request):
        """ Allows a user to rsvp a meetup """
        rsvp = {}
        keys_expected = ["user", "meetup", "response"]

        ret = self.helpers.is_valid_user_request(keys_expected, request)

        if ret[0] == 0:
            return ret[1], 400

        ret = self.helpers.is_blank_field(request)

        if ret[0] == 0:
            return ret[1], 400

        meetup = [m for m in self.meetups if m["id"] == meetup_id]

        if meetup:
            rsvp["id"] = len(self.rsvps) + 1
            rsvp["meetup"] = meetup_id
            rsvp["user"] = request.get_json()["user"]
            rsvp["response"] = request.get_json()["response"]
            self.rsvps.append(rsvp)
            return jsonify({"msg": "rsvp was created", "data": rsvp, "status": 201}), 201

        return jsonify({"msg": "Meetup was not found", "status": 404}), 404  

    def get_a_question(self, search_id):
        """ Returns a specific question record """

        if len(self.questions) == 0:
            return jsonify({"msg": "no questions were found", "data": self.questions, "status": 200}), 200      
        for question in self.questions:
            if question['id'] == search_id:
                return jsonify({"msg": "question was found", "data": question, "status": 200})     
        return jsonify({"msg": "question was not found", "data": [], "status": 404}), 404