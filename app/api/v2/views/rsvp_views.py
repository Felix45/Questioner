from flask import Blueprint, Flask, jsonify, request

from app.api.v2.models.meetups_model import UsersModel
from app.api.v2.models.rsvp_models import RsvpModel

rsvpV2 = Blueprint('rsvp_v2', __name__, url_prefix='/api/v2')

rsvps_model = RsvpModel()
users_model = UsersModel()


@rsvpV2.route('/meetups/<int:meetup_id>/rsvp/', methods=['POST'])
@users_model.token_required
def add_rsvp(meetup_id):
	return rsvps_model.rsvp_meetup(meetup_id, request)
