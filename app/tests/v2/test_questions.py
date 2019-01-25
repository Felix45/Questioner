""" Contains related tests to questions """

from app.tests.v2.basetest import SetUpTestClient
import datetime


class QuestionsTest(SetUpTestClient):

    def test_add_questions(self):
        meetup = {
                    "location": "PAC",
                    "images": ["hello.png", "wazito.jpg", "babayao.png"],
                    "topic": "Kilimani Mums",
                    "happeningOn": datetime.datetime(2019, 5, 17),
                    "Tags": ["women", "mums", "ladies"]
        }
        res = self.client.post("/api/v2/meetups", json=meetup, headers=self.headers)
        self.assertEqual(res.status_code, 201)
        question = {
            "meetup": 1,
            "title": "How do i install python in Ubuntu 18.04?",
            "body": "I have been trying to install python in ubuntu 18.04 with no success, someone help please."
        }
        res = self.client.post("/api/v2/questions", json=question,
                               headers=self.headers)
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
                               headers=self.headers)
        self.assertEqual(res.status_code, 201)
        res = self.client.patch("/api/v2/questions/1/upvote", json=question,
                                headers=self.headers)
        self.assertEqual(res.status_code, 201)
        self.assertIn("Update was successful", str(res.data))

        res = self.client.patch("/api/v2/questions/1/downvote", json=question,
                                headers=self.headers)
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
                               headers=self.headers)
        self.assertEqual(res.status_code, 201)
        res = self.client.post("/api/v2/questions", json=question_two,
                               headers=self.headers)
        self.assertEqual(res.status_code, 201)
        res = self.client.get("/api/v2/questions/1")
        self.assertEqual(res.status_code, 200)
        res = self.client.get("/api/v2/questions/2")
        self.assertEqual(res.status_code, 200)
        res = self.client.get("/api/v2/questions/100")
        self.assertEqual(res.status_code, 404)
