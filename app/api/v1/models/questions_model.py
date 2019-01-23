""" Manages all the meetup functions """
from datetime import date
from flask import Flask, request, jsonify
from app.api.v1.utils.user_validator import UsersHelper


class QuestionsModel():

    def __init__(self):
        self.questions = []
        self.helpers = UsersHelper()

    def add_a_question(self, user_request):
        """ Add a question record """
        question = {}
        keys_expected = ["user", "meetup", "title", "body"]

        result = self.helpers.is_valid_user_request(keys_expected, user_request)

        if result[0] == 0:
            return result[1], 400

        result = self.helpers.is_blank_field(user_request)

        if result[0] == 0:
            return result[1], 400
        question['id'] = len(self.questions) + 1
        question['votes'] = 0
        question['user'] = user_request.get_json()['user']
        question['meetup'] = user_request.get_json()['meetup']
        question['title'] = user_request.get_json()['title']
        question['body'] = user_request.get_json()['body']

        self.questions.append(question)
        return jsonify({"msg": "question was added", "data":self.questions, "status": 201}), 201

    def vote(self, vote, question_id, type):
        """ Allows a user to upvote or downvote a question """

        question = [quiz for quiz in self.questions if quiz["id"] == question_id]
      
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
