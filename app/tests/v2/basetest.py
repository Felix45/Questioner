''' Sets up the test client '''
import os
import unittest
from app.dbconnection import dbConn
from app import create_app


class SetUpTestClient(unittest.TestCase):
	def setUp(self):
		''' Sets up the test client for stackoverflowlite Api '''
		self.app = create_app('testing')
		self.client = self.app.test_client()
		self.user = {'username': 'Izzo', 'password': 'hello'}
		result = self.client.post("/api/v2/auth/login/", json=self.user, content_type='application/json')
		token = result.get_json()['token']
		self.headers = {"Content-Type": 'application/json'}
		self.headers["Authorization"] = "Bearer {}".format(token)
		
					
	def tearDown(self):
		''' Destroys the test client '''
		#dbConn.destroyTestDb()
		
if __name__ == '__main__':
	unittest.main(verbosity=1)
