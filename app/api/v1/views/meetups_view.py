from flask import Blueprint, Flask, jsonify, request

from app.api.v1.models.meetups_model import MeetUpsModel

meetupV1 = Blueprint('meetup_v1', __name__, url_prefix='/api/v1')

meetups_model = MeetUpsModel()


@meetupV1.route('/meetups', methods=['POST'])
def add_meetup():
	return meetups_model.add_meetup(request)


@meetupV1.route('/meetups/upcoming', methods=['GET'])
def get_meetup():
	return meetups_model.get_meetups()


@meetupV1.route('/meetups/<int:meetup_id>', methods=['GET'])
def get_a_meetup(meetup_id):
	return meetups_model.get_a_meetup(meetup_id)


@meetupV1.route('/questions', methods=['POST'])
def add_question():
	return meetups_model.add_a_question(request)


@meetupV1.route("/questions/<int:question_id>/upvote", methods=['PATCH'])
def up_vote(question_id):
	return meetups_model.vote(vote=1, question_id=question_id, type="upvote")


@meetupV1.route("/questions/<int:question_id>/downvote", methods=['PATCH'])
def down_vote(question_id):
	return meetups_model.vote(vote=-1, question_id=question_id, type="downvote")
