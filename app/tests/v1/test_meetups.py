""" Contains tests related to meetups """
from app.tests.v1.basetest import SetUpTestClient
import datetime


class MeetupTest(SetUpTestClient):

    def test_add_meetup(self):
        """ Adds a meetup record """
        meetup = {
                    "location": "Kileleshwa",
                    "images": ["hello.png", "wazito.jpg", "babayao.png"],
                    "topic": "Kilimani Mums",
                    "happeningOn": datetime.datetime(2019, 5, 17),
                    "Tags": ["women", "mums", "ladies"]
        }
        meetup_empty = {}

        meetup_two = {
                    "location": "",
                    "images": ["hello.png", "wazito.jpg", "babayao.png"],
                    "topic": "Kilimani Mums",
                    "happeningOn": datetime.datetime(2019, 5, 17),
                    "Tags": ["women", "mums", "ladies"]
        }

        res = self.client.post("/api/v1/meetups", json=meetup, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Meetup was added', str(res.data))

        res = self.client.post("/api/v1/meetups", json=meetup_two, content_type='application/json')
        self.assertEqual(res.status_code, 400)
        self.assertIn('location should be filled', str(res.data))

        res = self.client.post("/api/v1/meetups", json=meetup_empty,
                               content_type='application/json')
        self.assertEqual(res.status_code, 400)
        self.assertIn('sent an empty request', str(res.data))

    def test_get_all_meetups(self):
        """ Return all upcoming meetups """
        meetup = {
                "location": "Eldoret",
                "images": ["run.png", "marathon.jpg", "cross.png"],
                "topic": "Athletes",
                "happeningOn": datetime.datetime(2019, 5, 17),
                "Tags": ["sports", "IAAF", "AK"]
        }

        meetup_one = {
                "location": "",
                "images": ["lawyers.png", "doctors.jpg", "teachers.png"],
                "topic": "Career Talk",
                "happeningOn": datetime.datetime(2019, 5, 17),
                "Tags": ["law", "medicine", "Education"]
        }

        meetup_two = {
                "location": "IHUB",
                "images": ["coders.png", "developers.jpg", "facebook.png"],
                "topic": "Women in tech",
                "happeningOn": datetime.datetime(2019, 5, 17),
                "Tags": ["women", "mums", "ladies"]
        }
        res = self.client.post("/api/v1/meetups", json=meetup, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        res = self.client.post("/api/v1/meetups", json=meetup_one, content_type='application/json')
        self.assertEqual(res.status_code, 400)
        res = self.client.post("/api/v1/meetups", json=meetup_two, content_type='application/json')
        self.assertEqual(res.status_code, 200)

        res = self.client.get("/api/v1/meetups/upcoming")
        self.assertEqual(res.status_code, 200)

    def test_view_specific_meetup(self):
        """ Gets a specific meetup record """
        meetup = {
                "location": "Eldoret",
                "images": ["run.png", "marathon.jpg", "cross.png"],
                "topic": "Athletes",
                "happeningOn": datetime.datetime(2019, 5, 17),
                "Tags": ["sports", "IAAF", "AK"]
        }

        meetup_one = {
                "location": "Kileleshwa",
                "images": ["lawyers.png", "doctors.jpg", "teachers.png"],
                "topic": "Career Talk",
                "happeningOn": datetime.datetime(2019, 5, 17),
                "Tags": ["law", "medicine", "Education"]
        }
        res = self.client.post("/api/v1/meetups", json=meetup, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        res = self.client.post("/api/v1/meetups", json=meetup_one, content_type='application/json')
        self.assertEqual(res.status_code, 200)

        res = self.client.get("/api/v1/meetups/1")
        self.assertEqual(res.status_code, 200)

        res = self.client.get("/api/v1/meetups/2")
        self.assertEqual(res.status_code, 200)

        res = self.client.get("/api/v1/meetups/50")
        self.assertEqual(res.status_code, 404)
        self.assertIn('Meetup was not found', str(res.data))

    def test_add_questions(self):
        """ Tests adding a question """
        question = {

            "user": 1,
            "meetup": 1,
            "title": "How do i install python in Ubuntu 18.04?",
            "body": "I have been trying to install python in ubuntu 18.04 with no success, someone help please."
        }
        res = self.client.post("/api/v1/questions", json=question,
                               content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertIn('question was added', str(res.data))

    def test_vote_question(self):
        """ Allows user to upVote or downVote on a question """
        question = {
            "user": 1,
            "meetup": 1,
            "title": "How do i install python in Ubuntu 18.04?",
            "body": "I have been trying to install python in ubuntu\
                             18.04 with no success, someone help please."
        }
        res = self.client.post("/api/v1/questions", json=question,
                               content_type='application/json')
        self.assertEqual(res.status_code, 201)
        res = self.client.patch("/api/v1/questions/1/upvote", json=question,
                                content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn("upvote was successful", str(res.data))

        res = self.client.patch("/api/v1/questions/1/downvote", json=question,
                                content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn("downvote was successful", str(res.data))
 
    def test_rsvp_meetups(self):
        """ Allows users to confirm meetup attendance """
        meetup = {
                "location": "Eldoret",
                "images": ["run.png", "marathon.jpg", "cross.png"],
                "topic": "Athletes",
                "happeningOn": datetime.datetime(2019, 5, 17),
                "Tags": ["sports", "IAAF", "AK"]
        }

        meetup_one = {
                "location": "Kileleshwa",
                "images": ["lawyers.png", "doctors.jpg", "teachers.png"],
                "topic": "Career Talk",
                "happeningOn": datetime.datetime(2019, 5, 17),
                "Tags": ["law", "medicine", "Education"]
        }
        rsvp = {
                 "meetup": 1,
                 "user": 1,
                 "response": "Yes"
        }
        rsvp_two = {
                "meetup": 50,
                "user": 1,
                "response": "Yes"
        }
        res = self.client.post("/api/v1/meetups", json=meetup,
                               content_type='application/json')
        self.assertEqual(res.status_code, 200)
        res = self.client.post("/api/v1/meetups", json=meetup_one,
                               content_type='application/json')
        self.assertEqual(res.status_code, 200)

        res = self.client.post("/api/v1/meetups/1/rsvp", json=rsvp,
                               content_type='application/json')
        self.assertEqual(res.status_code, 201)
        res = self.client.post("/api/v1/meetups/50/rsvp", json=rsvp_two,
                               content_type='application/json')
        self.assertEqual(res.status_code, 404)

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
        res = self.client.post("/api/v1/questions", json=question,
                               content_type='application/json')
        self.assertEqual(res.status_code, 201)
        res = self.client.post("/api/v1/questions", json=question_two,
                               content_type='application/json')
        self.assertEqual(res.status_code, 201)
        res = self.client.get("/api/v1/questions/1")
        self.assertEqual(res.status_code, 200)
        res = self.client.get("/api/v1/questions/2")
        self.assertEqual(res.status_code, 200)
        res = self.client.get("/api/v1/questions/100")
        self.assertEqual(res.status_code, 404)
