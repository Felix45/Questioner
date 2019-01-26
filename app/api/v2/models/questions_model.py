""" Manages all the meetup functions """
from datetime import date
import json
import jwt
from flask import Flask, request, jsonify
from app.api.v2.utils.user_validator import UsersHelper
from app.api.v2.utils.database_helper import DatabaseHelper
from app.api.v2.models.users_model import UsersModel

database = DatabaseHelper()


class QuestionsModel():

    def __init__(self):
        self.questions = []
        self.helpers = UsersHelper()

    def add_a_question(self, user_request):
        """ Add a question record """
        keys_expected = ["meetup", "title", "body"]

        token = request.headers.get('Authorization').split()[1]
        user_id = jwt.decode(token, 'Felix45', algorithms=['HS256'])

        result = self.helpers.is_valid_user_request(keys_expected, user_request)
        
        if result[0] == 0:
            return result[1], 400

        result = self.helpers.is_blank_field(user_request)

        if result[0] == 0:
            return result[1], 400
        data = user_request.get_json()
        
        data['votes'] = 0
        columns = 'created_by,meetup_id,title,body,votes'
        rows = "%d, %d, %s, %s, %d" % (user_id['user'],data['meetup'],"'"+data['title']+"'","'"+data['body']+"'",data['votes'])
       
        if database.find_in_db('users', 'id=%d'%(user_id['user'],)) and database.find_in_db('meetups', 'Id=%d'%(data['meetup'],)):
            return database.insert_into_db('questions', columns, rows, 'question')
        return jsonify({'msg':'Question was not added'}), 400
        
    def vote(self, question_id, type):
        """ Allows a user to upvote or downvote a question """
        question = database.find_in_db('questions','id=%d'%(question_id,))
        
        if question and type == 'upvote':
            expression = "votes=votes+1"
            database.update_columns_record('questions', expression, 'id', question_id)
        elif question and type == 'downvote':
            expression = "votes=votes-1"
            database.update_columns_record('questions', expression, 'id', question_id)
        else:
            return jsonify({"msg": "Question was not found", "status": 404}), 404 

        question = database.find_in_db('questions','id=%d'%(question_id,))    
        return jsonify({"msg": "{} was successful".format(type),
                            "status": 201, "data": question}), 201

    def get_a_question(self, search_id):
        """ Returns a specific question record """
        question = database.find_in_db('questions', 'id=%d' % (search_id))
        if question:
            return jsonify({"msg": "Question was found", "data": question, "status":200}), 200
        return jsonify({"msg": "Question was not found", "data":question, "status": 404}), 404
