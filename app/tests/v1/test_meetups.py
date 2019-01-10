""" Contains tests related to meetups """
from app.tests.v1.basetest import SetUpTestClient
import datetime

class MeetupTest(SetUpTestClient):

    def test_add_meetup(self):
        """ Adds a meetup record """
        meetup = {
                    "location" : "Kileleshwa",
                    "images"   : ["hello.png" , "wazito.jpg" , "babayao.png"],
                    "topic"    : "Kilimani Mums",
                    "happeningOn" : datetime.datetime(2019, 5, 17),
                    "Tags"         : ["women","mums","ladies"]
        }
        meetup_empty = {}

        meetup_two = {
                    "location" : "",
                    "images"   : ["hello.png" , "wazito.jpg" , "babayao.png"],
                    "topic"    : "Kilimani Mums",
                    "happeningOn" : datetime.datetime(2019, 5, 17),
                    "Tags"         : ["women","mums","ladies"]
        }

        res = self.client.post("/api/v1/meetups",json=meetup,content_type='application/json')
        self.assertEqual(res.status_code,200)
        self.assertIn('user was added',res.data)

        res = self.client.post("/api/v1/meetups",json=meetup_two,content_type='application/json')
        self.assertEqual(res.status_code,400)
        self.assertIn('Field value was empty:',res.data)

        res = self.client.post("/api/v1/meetups",json=meetup_empty,content_type='application/json')
        self.assertEqual(res.status_code,400)
        self.assertIn('sent an empty request',res.data)

        def test_get_all_meetups():
            meetup = {
                    "location" : "Kileleshwa",
                    "images"   : ["hello.png" , "wazito.jpg" , "babayao.png"],
                    "topic"    : "Kilimani Mums",
                    "happeningOn" : datetime.datetime(2019, 5, 17),
                    "Tags"         : ["women","mums","ladies"]
            }

            meetup_one = {
                    "location" : "Kileleshwa",
                    "images"   : ["hello.png" , "wazito.jpg" , "babayao.png"],
                    "topic"    : "Kilimani Mums",
                    "happeningOn" : datetime.datetime(2019, 5, 17),
                    "Tags"         : ["women","mums","ladies"]
            }

            meetup_two = {
                    "location" : "Kileleshwa",
                    "images"   : ["hello.png" , "wazito.jpg" , "babayao.png"],
                    "topic"    : "Kilimani Mums",
                    "happeningOn" : datetime.datetime(2019, 5, 17),
                    "Tags"         : ["women","mums","ladies"]
            }
            res = self.client.post("/api/v1/meetups",json=meetup,content_type='application/json')
            self.assertEqual(res.status_code,200)
            res = self.client.post("/api/v1/meetups",json=meetup_one,content_type='application/json')
            self.assertEqual(res.status_code,200)
            res = self.client.post("/api/v1/meetups",json=meetup_two,content_type='application/json')
            self.assertEqual(res.status_code,200)

            res = self.client.get("/api/v1/meetups/upcoming",json=meetup,content_type='application/json')
            self.assertEqual(res.status_code,200)

