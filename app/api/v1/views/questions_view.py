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


@questionV1.route("/questions/<int:question_id>/<string:vote>", methods=['PATCH'])
def vote(question_id, vote):
	return questions_model.vote(question_id=question_id, type=vote)
