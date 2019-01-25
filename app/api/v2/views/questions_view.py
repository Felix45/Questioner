from flask import Blueprint, Flask, jsonify, request

from app.api.v2.models.questions_model import QuestionsModel
from app.api.v2.models.questions_model import UsersModel

questionV2 = Blueprint('question_v2', __name__, url_prefix='/api/v2')

questions_model = QuestionsModel()
users_model = UsersModel()


@questionV2.route('/questions', methods=['POST'])
@users_model.token_required
def add_question():
	return questions_model.add_a_question(request)

@questionV2.route('/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):
	return questions_model.get_a_question(question_id)


@questionV2.route("/questions/<int:question_id>/<string:vote>", methods=['PATCH'])
@users_model.token_required
def vote(question_id, vote):
	return questions_model.vote(question_id, vote)

