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
        self.assertIn('user was added', res.data)

        res = self.client.post("/api/v1/meetups", json=meetup_two, content_type='application/json')
        self.assertEqual(res.status_code, 400)
        self.assertIn('Field value was empty:', res.data)

        res = self.client.post("/api/v1/meetups", json=meetup_empty,
                               content_type='application/json')
        self.assertEqual(res.status_code, 400)
        self.assertIn('sent an empty request', res.data)

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
        self.assertIn('user was not found', res.data)
