from flask import Flask, jsonify
import re


class UsersHelper:
	def __init__(self):
		''' Contains helper methods for UsersModel class '''
		pass
		
	def is_valid_user_request(self, keys_expected, user_request):
		if len(user_request.get_json().keys()) == 0:
			return 0, 'sent an empty request'
			
		sent_keys = user_request.get_json().keys()
		
		for key in keys_expected:
			if key not in sent_keys:
				return 0, 'You must provide a {}'.format(key)

		return 1	, 'user request was valid'
		
	def is_blank_field(self, user_request):
		
		for key, user_item in user_request.get_json().items():
			if user_item == '':
				return False, 'Field value was empty: {}'.format(key)
				
		return True, ''
		
	def is_available(self, value, key, users, user_id=0):
		for user in users:
			if user[key] == value and user_id != user['user_id']:
				return False, jsonify({'message': '{} field value is not available: '.format(key)})
		
		return True, jsonify({'message': ''})
		
	def is_valid_email(self, email):
		if re.match("\A(?P<name>[\w\-_]+)@(?P<domain>[\w\-_]+).(?P<toplevel>[\w]+)\Z", email, re.IGNORECASE) and len(email) > 7:
			return True, jsonify({'message': ''})
		return False, jsonify({'message': 'email is not valid:'})
			
	def is_valid_password(self, password, cpassword):
		if password == cpassword:
			if re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{6,12}$", password):
				return True, jsonify({'message': ''})
			return False, jsonify({'message': 'Password should have at least 5 characters, a lowercase, an uppercase and a special character e.g Felix45@ or Emily16#'})
		else:
			return False, jsonify({'message': 'Confirm password provided did not match password'})
			