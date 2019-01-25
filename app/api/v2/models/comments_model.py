""" Manages all the meetup functions """
import datetime
from datetime import date
import json
import jwt
from flask import Flask, request, jsonify
from app.api.v2.utils.user_validator import UsersHelper
from app.api.v2.models.users_model import UsersModel
from app.api.v2.utils.database_helper import DatabaseHelper


database = DatabaseHelper()


class CommentsModel():

    def __init__(self):
        ''' Contains all that is related to comments '''
        self.helpers = UsersHelper()

    def add_comment(self, user_request):
        ''' Adds a comment to a question '''
        keys_expected = ['question_id', 'comment']
        result = self.helpers.is_valid_user_request(keys_expected,
                                                    user_request)

        if result[0] == 0:
            return result[1], 400

        result = self.helpers.is_blank_field(user_request)

        if result[0] == 0:
            return result[1], 400
        data = user_request.get_json()
        token = request.headers.get('Authorization').split()[1]
        user_id = jwt.decode(token, 'Felix45', algorithms=['HS256'])
        
        if not UsersModel().get_logged_in_user(user_id):
            return jsonify({'msg': 'You can not add a meetup', 'status': 403}), 403
        data['user_id'] = user_id['user']
        valid_user = database.find_in_db("users", "Id=%d" % (user_id['user']))
        valid_question = database.find_in_db('questions', 'Id=%d'
                                             % (data['question_id']))
                                             
        if len(valid_user) == 0 or len(valid_question) == 0:
            return jsonify({'error': 'Either question or users does not exist'
                            , 'status': 404}), 404

        return self.insert_comment(data)

    def insert_comment(self, data):

        columns = 'created_by,question_id,comment,created_on'
        rows = "%d, %d, '%s', '%s' " % (data['user_id'], data['question_id'],
                                    data['comment'],
                                    str(datetime.datetime.now())
                                    )
        return database.insert_into_db('comments', columns, rows, 'comment')
