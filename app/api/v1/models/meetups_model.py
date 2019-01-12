""" Manages all the meetup functions """
from datetime import date
from flask import Flask, request, jsonify
from app.api.v1.utils.user_validator import UsersHelper


class MeetUpsModel():

    def __init__(self):
        self.meetups = []
        self.questions = []
        self.helpers = UsersHelper()

    def add_meetup(self, user_request):
        user = {}

        keys_expected = ["location", "images", "topic", "happeningOn", "Tags"]

        ret = self.helpers.is_valid_user_request(keys_expected, user_request)

        if ret[0] == 0:
            return ret[1], 400

        ret = self.helpers.is_blank_field(user_request)

        if ret[0] == 0:
            return ret[1], 400

        user["id"] = len(self.meetups) + 1
        user["created_on"] = date.today()
        user["location"] = user_request.get_json()["location"]
        user["images"] = user_request.get_json()["images"]
        user["topic"] = user_request.get_json()["topic"]
        user["happeningOn"] = user_request.get_json()["happeningOn"]
        user["Tags"] = user_request.get_json()["Tags"]

        self.meetups.append(user)

        return jsonify({"msg": "user was added", "data": self.meetups, "status": 200})

    def get_meetups(self):
        if len(self.meetups) == 0:
            return jsonify({"msg": "no users were found", "data": self.meetups, "status": 200})
        return jsonify({"msg": "users", "data": self.meetups, "status": 200})

    def get_a_meetup(self, search_id):
        """ Returns a specific meetup record """

        if len(self.meetups) == 0:
            return jsonify({"msg": "no users were found", "data": self.meetups, "status": 200}), 200
        else:
            for meetup in self.meetups:
                if meetup['id'] == search_id:
                    return jsonify({"msg": "user was found", "data": meetup, "status": 200})     
        return jsonify({"msg": "user was not found", "data": [], "status": 404}), 404

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
        question['user'] = user_request.get_json()['user']
        question['meetup'] = user_request.get_json()['meetup']
        question['title'] = user_request.get_json()['title']
        question['body'] = user_request.get_json()['body']

        self.questions.append(question)
        return jsonify({"msg": "question was added", "status": 201}), 201
