''' Sets up the test client '''
import os
import unittest
from app import create_app
from app.dbconnection import dbConn


class SetUpTestClient(unittest.TestCase):
	def setUp(self):
		''' Sets up the test client for stackoverflowlite Api '''
		self.app = create_app('testing')
		self.client = self.app.test_client()
		os.environ['FLASK_ENV'] = 'testing'
		print os.getenv('FLASK_ENV')
		dbConn.setUpTestDb()
					
	def tearDown(self):
		''' Destroys the test client '''
		#self.dbconn.destroyTestDb()
		
if __name__ == '__main__':
	unittest.main(verbosity=1)
