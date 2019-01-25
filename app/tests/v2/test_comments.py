""" Contains tests related to meetups """
from app.tests.v2.basetest import SetUpTestClient
import datetime


class CommentTest(SetUpTestClient):

    def test_add_comment(self):
        """ Adds a comment record """
        meetup = {
                    "location": "Kileleshwa",
                    "images": ["hello.png", "wazito.jpg", "babayao.png"],
                    "topic": "Kilimani Mums",
                    "happeningOn": datetime.datetime(2019, 5, 17),
                    "Tags": ["women", "mums", "ladies"]
        }
        res = self.client.post("/api/v2/meetups", json=meetup, headers=self.headers)
        print(res.data)
        question = {
            "title": "How do i install python in Ubuntu 18.04?",
            "body": "I have been trying to install python in ubuntu 18.04 with no success, someone help please."
        }
        res = self.client.post("/api/v2/questions", json=question,
                               headers=self.headers)

        comment = {
                "question_id": 1,
                "comment": "This comment should go to a question"
        }

        comment_empty = {}

        comment_two = {
                "question_id": 1,
                "comment": ""
        }

        res = self.client.post("/api/v2/comments", json=comment, headers=self.headers)
        self.assertEqual(res.status_code, 201)
        self.assertIn('comment added successfully', str(res.data))

        res = self.client.post("/api/v2/comments", json=comment_two, headers=self.headers)
        self.assertEqual(res.status_code, 400)
        self.assertIn('Field value was empty:', str(res.data))

        res = self.client.post("/api/v2/comments", json=comment_empty,
                               headers=self.headers)
        self.assertEqual(res.status_code, 400)
        self.assertIn('sent an empty request', str(res.data))
  