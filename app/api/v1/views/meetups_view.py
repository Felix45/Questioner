from flask import Blueprint, Flask , jsonify , request 

from app.api.v1.models.meetups_model import MeetUpsModel

meetupV1 = Blueprint('meetup_v1',__name__,url_prefix='/api/v1')

meetups_model = MeetUpsModel()

@meetupV1.route('/meetups', methods=['POST'])
def add_meetup():
	return meetups_model.add_meetup(request)
