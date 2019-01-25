from flask import Blueprint, Flask, jsonify, request

from app.api.v2.models.meetups_model import MeetUpsModel
from app.api.v2.models.meetups_model import UsersModel
from app.api.v2.models.rsvp_models import RsvpModel

meetupV2 = Blueprint('meetup_v2', __name__, url_prefix='/api/v2')

meetups_model = MeetUpsModel()
users_model = UsersModel()


@meetupV2.route('/meetups', methods=['POST'])
@users_model.token_required
def add_meetup():
	return meetups_model.add_meetup(request)


@meetupV2.route('/meetups/delete/<int:id>', methods=['DELETE'])
@users_model.token_required
def delete_meetup(id):
	return meetups_model.delete_meetup(id)



@meetupV2.route('/meetups/upcoming', methods=['GET'])
def get_meetup():
	return meetups_model.get_meetups()


@meetupV2.route('/meetups/<int:meetup_id>', methods=['GET'])
def get_a_meetup(meetup_id):
	return meetups_model.get_a_meetup(meetup_id)

