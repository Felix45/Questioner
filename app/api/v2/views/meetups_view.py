from flask import Blueprint, Flask, jsonify, request

from app.api.v2.models.meetups_model import MeetUpsModel
from app.api.v2.models.users_model import UsersModel

meetupV2 = Blueprint('meetup_v2', __name__, url_prefix='/api/v2')

meetups_model = MeetUpsModel()
users_model   = UsersModel()


@meetupV2.route('/meetups', methods=['POST'])
@users_model.token_required
def add_meetup():
	return meetups_model.add_meetup(request)


@meetupV2.route('/meetups/upcoming', methods=['GET'])
def get_meetup():
	return meetups_model.get_meetups()

@meetupV2.route('/meetups/delete/<int:meetup_id>', methods=['DELETE'])
def delete_meetup(meetup_id):
	return meetups_model.delete_meetup(meetup_id)


@meetupV2.route('/meetups/<int:meetup_id>', methods=['GET'])
def get_a_meetup(meetup_id):
	return meetups_model.get_a_meetup(meetup_id)


@meetupV2.route('/questions', methods=['POST'])
def add_question():
	return meetups_model.add_a_question(request)

@meetupV2.route('/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):
	return meetups_model.get_a_question(question_id)


@meetupV2.route("/questions/<int:question_id>/upvote", methods=['PATCH'])
def up_vote(question_id):
	return meetups_model.vote(vote=1, question_id=question_id, type="upvote")


@meetupV2.route("/questions/<int:question_id>/downvote", methods=['PATCH'])
def down_vote(question_id):
	return meetups_model.vote(vote=-1, question_id=question_id, type="downvote")


@meetupV2.route("/meetups/<int:meetup_id>/rsvp", methods=['POST'])
def rsvp_meetup(meetup_id):
	return meetups_model.rsvp_meetup(meetup_id, request)


