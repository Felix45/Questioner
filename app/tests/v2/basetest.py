''' Sets up the test client '''
import unittest
from app import create_app


class SetUpTestClient(unittest.TestCase):
	def setUp(self):
		''' Sets up the test client for stackoverflowlite Api '''
		self.app = create_app()
		self.client = self.app.test_client()
		
	def tear_down(self):
		''' Destroys the test client '''
		self.app.testing = False
		self.app = None
		
if __name__ == '__main__':
	unittest.main(verbosity=1)
