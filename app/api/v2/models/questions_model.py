""" Manages all the meetup functions """
from datetime import date
import json
from flask import Flask, request, jsonify
from app.api.v1.utils.user_validator import UsersHelper
from app.api.v2.utils.database_helper import DatabaseHelper
from app.api.v2.models.users_model import UsersModel

database = DatabaseHelper()

class QuestionsModel():

    def __init__(self):
        self.questions = []
        self.helpers = UsersHelper()

    def add_a_question(self, user_request):
        """ Add a question record """
        keys_expected = ["user", "meetup", "title", "body"]

        ret = self.helpers.is_valid_user_request(keys_expected, user_request)

        if ret[0] == 0:
            return ret[1], 400

        ret = self.helpers.is_blank_field(user_request)

        if ret[0] == 0:
            return ret[1], 400
        data = user_request.get_json()
        data['votes']=0
        columns = 'created_by,meetup_id,title,body,votes'
        rows="%d, %d, %s, %s, %d" %( data['user'],data['meetup'],"'"+data['title']+"'","'"+data['body']+"'",data['votes'])
        #rows=""+data['user']+", "+data['meetup']+", '"+data['title']+"','"+data['body']+"', "+data['votes']+""
        
        if database.find_in_db('users', 'id=%d'%(data['user'],)) and database.find_in_db('meetups', 'Id=%d'%(data['meetup'],)):
            return database.insert_into_db('questions', columns, rows, 'question')
        return jsonify({'msg':'Question was not added'}), 400
        

    def vote(self, vote, question_id, type):
        """ Allows a user to upvote or downvote a question """

        question = [q for q in self.questions if q["id"] == question_id]
      
        if question:
            question[0]["votes"] = int(question[0]["votes"]) + int(vote)
            question[0]["votes"] = 0 if question[0]["votes"] < 0 else question[0]["votes"]
            return jsonify({"msg": "{} was successful".format(type),
                            "status": 201, "data": self.questions}), 201

        return jsonify({"msg": "Question was not found", "status": 404}), 404  

    def get_a_question(self, search_id):
        """ Returns a specific question record """

        if len(self.questions) == 0:
            return jsonify({"msg": "no questions were found", "data": self.questions, "status": 200}), 200      
        for question in self.questions:
            if question['id'] == search_id:
                return jsonify({"msg": "question was found", "data": question, "status": 200})     
        return jsonify({"msg": "question was not found", "data": [], "status": 404}), 404