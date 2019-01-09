""" Setup tests for users """
from app.tests.v1.basetest import SetUpTestClient
from app.tests.v1.user_list import *


class UsersModelTest(SetUpTestClient):
    """ Setup tests for user endpoints """
    def test_get_users(self):
		res = self.client.post("/api/v1/users/list/")
		self.assertEqual(res.status_code, 200)

    def test_add_user(self):
        res = self.client.post("/api/v1/users/add/",json=user_1,content_type='application/json')
        self.assertEqual(res.status_code,400)
