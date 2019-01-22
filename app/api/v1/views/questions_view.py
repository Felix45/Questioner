from flask import Blueprint, Flask, jsonify, request

from app.api.v1.models.questions_model import QuestionsModel

questionV1 = Blueprint('question_v1', __name__, url_prefix='/api/v1')

questions_model = QuestionsModel()



@questionV1.route('/questions', methods=['POST'])
def add_question():
	return questions_model.add_a_question(request)

@questionV1.route('/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):
	return questions_model.get_a_question(question_id)


@questionV1.route("/questions/<int:question_id>/upvote", methods=['PATCH'])
def up_vote(question_id):
	return questions_model.vote(vote=1, question_id=question_id, type="upvote")


@questionV1.route("/questions/<int:question_id>/downvote", methods=['PATCH'])
def down_vote(question_id):
	return questions_model.vote(vote=-1, question_id=question_id, type="downvote")

