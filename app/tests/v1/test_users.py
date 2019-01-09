""" Setup tests for users """
from app.tests.v1.basetest import SetUpTestClient
from app.tests.v1.user_list import *


class UsersModelTest(SetUpTestClient):
    """ Setup tests for user endpoints """
    def test_get_users(self):
		    res = self.client.get("/api/v1/users/list/")
		    self.assertEqual(res.status_code, 200)

    def test_user_missing_fields(self):
		
		res = self.client.post("/api/v1/users/add/",json=user_1,content_type='application/json')
		self.assertEqual(res.status_code,400)
		self.assertIn('sent an empty request',res.data)

    def test_blank_values(self):
		
		res = self.client.post("/api/v1/users/add/",json=user_2,content_type='application/json')
		self.assertEqual(res.status_code,400)
		self.assertIn('Field value was empty:',res.data)
		
    def test_is_available(self):
		
		self.client.post("/api/v1/users/add/",json=user_4,content_type='application/json')
		res = self.client.post("/api/v1/users/add/",json=user_5,content_type='application/json')
		self.assertEqual(res.status_code,409)
		self.assertIn('username field value is not available:',res.data)
		
		
		
    def test_is_valid_password(self):
		res = self.client.post("/api/v1/users/add/",json=user_10,content_type='application/json')
		self.assertEqual(res.status_code,400)

		self.assertIn('Confirm password provided did not match password',res.data)
		res = self.client.post("/api/v1/users/add/",json=user_11,content_type='application/json')
		self.assertEqual(res.status_code,200)



    def test_add_user(self):
        res = self.client.post("/api/v1/users/add/",json=user_1,content_type='application/json')
        self.assertEqual(res.status_code,400)
