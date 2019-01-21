""" Contains related tests to questions """

from app.tests.v2.basetest import SetUpTestClient
import datetime


class MeetupTest(SetUpTestClient):

    def test_add_questions(self):
        question = {

            "user": 1,
            "meetup": 1,
            "title": "How do i install python in Ubuntu 18.04?",
            "body": "I have been trying to install python in ubuntu 18.04 with no success, someone help please."
        }
        res = self.client.post("/api/v2/questions", json=question,
                               content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertIn('question added', str(res.data))

    def test_vote_question(self):
        """ Allows user to upVote or downVote on a question """
        question = {
            "user": 1,
            "meetup": 1,
            "title": "How do i install python in Ubuntu 18.04?",
            "body": "I have been trying to install python in ubuntu\
                             18.04 with no success, someone help please."
        }
        res = self.client.post("/api/v2/questions", json=question,
                               content_type='application/json')
        self.assertEqual(res.status_code, 201)
        res = self.client.patch("/api/v2/questions/1/upvote", json=question,
                                content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn("Update was successful", str(res.data))

        res = self.client.patch("/api/v2/questions/1/downvote", json=question,
                                content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn("Update was successful", str(res.data))

    def test_get_a_question(self):
        """ Allows a user to fetch a specific question """
        question = {
                "user": 1,
                "meetup": 1,
                "title": "How do i install python in Ubuntu 18.04?",
                "body": "I have been trying to install python in ubuntu\
                                        18.04 with no success, someone help please."
        }
        question_two = {
                "user": 1,
                "meetup": 1,
                "title": "How do i install python in Ubuntu 18.04?",
                "body": "I have been trying to install python in ubuntu\
                                18.04 with no success, someone help please."
        }
        res = self.client.post("/api/v2/questions", json=question,
                               content_type='application/json')
        self.assertEqual(res.status_code, 201)
        res = self.client.post("/api/v2/questions", json=question_two,
                               content_type='application/json')
        self.assertEqual(res.status_code, 201)
        res = self.client.get("/api/v2/questions/1")
        self.assertEqual(res.status_code, 200)
        res = self.client.get("/api/v2/questions/2")
        self.assertEqual(res.status_code, 200)
        res = self.client.get("/api/v2/questions/100")
        self.assertEqual(res.status_code, 404)
 