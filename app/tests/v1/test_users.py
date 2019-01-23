""" Setup tests for users """
from app.tests.v1.basetest import SetUpTestClient
from app.tests.v1.user_list import *


class UsersModelTest(SetUpTestClient):
		""" Setup tests for user endpoints """
		def test_get_users(self):
			bad_token = {'token': 'hdhdkfjdkfkdfkdfdkfkdf'}
			res = self.client.get("/api/v1/users/list/", json=bad_token, content_type='application/json')
			self.assertEqual(res.status_code, 403)

		def test_user_missing_fields(self):

			res = self.client.post("/api/v1/users/add/", json=user_1, content_type='application/json')
			self.assertEqual(res.status_code, 400)
			self.assertIn('sent an empty request', str(res.data))

		def test_blank_values(self):
			""" Tests blank field values """
			res = self.client.post("/api/v1/users/add/", json=user_2, content_type='application/json')
			self.assertEqual(res.status_code, 400)
			self.assertIn('Field value was empty:', str(res.data))

		def test_is_available(self):
		
			self.client.post("/api/v1/users/add/", json=user_4, content_type='application/json')
			res = self.client.post("/api/v1/users/add/", json=user_5, content_type='application/json')
			self.assertEqual(res.status_code, 409)
			self.assertIn('username field value is not available:', str(res.data))
			
		def test_is_valid_password(self):
			res = self.client.post("/api/v1/users/add/", json=user_10, content_type='application/json')
			self.assertEqual(res.status_code, 400)

			self.assertIn('Confirm password provided did not match password', str(res.data))
			res = self.client.post("/api/v1/users/add/", json=user_11, content_type='application/json')
			self.assertEqual(res.status_code, 201)

		def test_add_user(self):
				res = self.client.post("/api/v1/users/add/", json=user_1, content_type='application/json')
				self.assertEqual(res.status_code, 400)

		def test_user_login(self):
			self.client.post("/api/v1/users/add/", json=user_login_0, content_type='application/json')

			res = self.client.post("/api/v1/auth/login/", json=user_login_1,
								   content_type='application/json')
			self.assertEqual(res.status_code, 400)
			self.assertIn('sent an empty request', str(res.data))

			res = self.client.post("/api/v1/auth/login/", json=user_login_2,
								   content_type='application/json')
			self.assertEqual(res.status_code, 400)

			res = self.client.post("/api/v1/auth/login/", json=user_login_3, content_type='application/json')
			self.assertEqual(res.status_code, 200)
