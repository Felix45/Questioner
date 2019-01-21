''' Sets up the test client '''
import unittest
from app import create_app
from app.dbconnection import DbConnection


class SetUpTestClient(unittest.TestCase):
	def setUp(self):
		''' Sets up the test client for stackoverflowlite Api '''
		self.app = create_app('testing')
		self.client = self.app.test_client()
		with self.app.app_context():
			self.db = DbConnection().setUpTestDb()
		
	def tear_down(self):
		''' Destroys the test client '''
		with self.app.app_context():
			DbConnection().destroyTestDb()
		
if __name__ == '__main__':
	unittest.main(verbosity=1)
