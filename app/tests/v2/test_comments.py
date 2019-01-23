""" Contains tests related to meetups """
from app.tests.v2.basetest import SetUpTestClient
import datetime


class CommentTest(SetUpTestClient):

    def test_add_comment(self):
        """ Adds a comment record """

        comment = {
                "user_id": 1,
                "question_id": 1,
                "comment": "This comment should go to a question"
        }

        comment_empty = {}

        comment_two = {
                "user_id": 1,
                "question_id": 1,
                "comment": ""
        }

        res = self.client.post("/api/v2/comments", json=comment, content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertIn('comment added successfully', str(res.data))

        res = self.client.post("/api/v2/comments", json=comment_two, content_type='application/json')
        self.assertEqual(res.status_code, 400)
        self.assertIn('Field value was empty:', str(res.data))

        res = self.client.post("/api/v2/comments", json=comment_empty,
                               content_type='application/json')
        self.assertEqual(res.status_code, 400)
        self.assertIn('sent an empty request', str(res.data))

    