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


@meetupV1.route("/meetups/<int:meetup_id>/rsvp", methods=['POST'])
def rsvp_meetup(meetup_id):
	return meetups_model.rsvp_meetup(meetup_id, request)
