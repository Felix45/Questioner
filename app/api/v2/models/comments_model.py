""" Manages all the meetup functions """
import datetime
from datetime import date
import json
from flask import Flask, request, jsonify
from app.api.v2.utils.user_validator import UsersHelper
from app.api.v2.utils.database_helper import DatabaseHelper


database = DatabaseHelper()


class CommentsModel():

    def __init__(self):
        ''' Contains all that is related to comments '''
        self.helpers = UsersHelper()

    def add_comment(self, user_request):
        ''' Adds a comment to a question '''
        keys_expected = ['user_id', 'question_id', 'comment']
        result = self.helpers.is_valid_user_request(keys_expected,
                                                    user_request)

        if result[0] == 0:
            return result[1], 400

        result = self.helpers.is_blank_field(user_request)

        if result[0] == 0:
            return result[1], 400
        data = user_request.get_json()
        valid_user = database.find_in_db("users", "Id=%d" % (data['user_id']))
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
