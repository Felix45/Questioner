""" Manages all the meetup functions """
from datetime import date
from flask import Flask, request, jsonify
from app.api.v1.utils.user_validator import UsersHelper


class MeetUpsModel():

    def __init__(self):
        self.meetups = []
        self.questions = []
        self.rsvps = []
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

        return jsonify({"msg": "Meetup was added", "data": self.meetups, "status": 201})

    def get_meetups(self):
        if len(self.meetups) == 0:
            return jsonify({"msg": "no meetups were found", "data": self.meetups, "status": 200})
        return jsonify({"msg": "meetups", "data": self.meetups, "status": 200})

    def get_a_meetup(self, search_id):
        """ Returns a specific meetup record """

        if len(self.meetups) == 0:
            return jsonify({"msg": "no meetups were found", "data": self.meetups, "status": 200}), 200      
        for meetup in self.meetups:
            if meetup['id'] == search_id:
                return jsonify({"msg": "Meetup was found", "data": meetup, "status": 200})     
        return jsonify({"msg": "Meetup was not found", "data": [], "status": 404}), 404

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
