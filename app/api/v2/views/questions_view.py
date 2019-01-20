from flask import Blueprint, Flask, jsonify, request

from app.api.v2.models.questions_model import QuestionsModel

questionV2 = Blueprint('question_v2', __name__, url_prefix='/api/v2')

questions_model = QuestionsModel()


@questionV2.route('/questions', methods=['POST'])
def add_question():
	return questions_model.add_a_question(request)

@questionV2.route('/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):
	return questions_model.get_a_question(question_id)


@questionV2.route("/questions/<int:question_id>/upvote", methods=['PATCH'])
def up_vote(question_id):
	return questions_model.vote(vote=1, question_id=question_id, type="upvote")


@questionV2.route("/questions/<int:question_id>/downvote", methods=['PATCH'])
def down_vote(question_id):
	return questions_model.vote(vote=-1, question_id=question_id, type="downvote")


