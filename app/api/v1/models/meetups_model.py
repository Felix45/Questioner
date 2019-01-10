""" Manages all the meetup functions """
from datetime import date
from flask import Flask, request, jsonify

class MeetUpsModel():

    def __init__(self):
        self.meetups = []

    def add_meetup(self,user_request):
        user = {}

        

        user["id"] = len(self.meetups) + 1
        user["created_on"]  = date.today()
        user["location"]    = user_request.get_json()["location"]
        user["images"]      = user_request.get_json()["images"]
        user["topic"]       = user_request.get_json()["topic"]
        user["happeningOn"] = user_request.get_json()["happeningOn"]
        user["Tags"]        = user_request.get_json()["Tags"]

        self.meetups.append(user)

        return jsonify({"msg":"user was added","data":self.meetups})


