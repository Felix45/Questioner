""" Manages all the meetup functions """
from datetime import date
from flask import Flask, request, jsonify
from app.api.v1.utils.user_validator import UsersHelper

class MeetUpsModel():

    def __init__(self):
        self.meetups = []
        self.helpers = UsersHelper()

    def add_meetup(self,user_request):
        user = {}

        keys_expected = ["location","images","topic","happeningOn","Tags"]

        ret = self.helpers.is_valid_user_request(keys_expected,user_request)

        if ret[0] == 0:
            return ret[1]  , 400


        ret = self.helpers.is_blank_field(user_request)

        if ret[0] == 0:
            return ret[1] , 400

        user["id"] = len(self.meetups) + 1
        user["created_on"]  = date.today()
        user["location"]    = user_request.get_json()["location"]
        user["images"]      = user_request.get_json()["images"]
        user["topic"]       = user_request.get_json()["topic"]
        user["happeningOn"] = user_request.get_json()["happeningOn"]
        user["Tags"]        = user_request.get_json()["Tags"]

        self.meetups.append(user)

        return jsonify({"msg":"user was added","data":self.meetups})


