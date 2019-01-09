""" Contains tests related to meetups """
from app.tests.v1.basetest import SetUpTestClient
from datetime import date

class MeetupTest(SetUpTestClient):

    def add_meet_up(self):
        """ Adds a meetup record """
        meetup = {
                    "location" : "Kileleshwa",
                    "images"   : ["hello.png" , "wazito.jpg" , "babayao.png"],
                    "topic"    : "Kilimani Mums",
                    "happeningOn" : date.today(),
                    "Tags"         : ["women","mums","ladies"]

        }

        
        res = self.client.post("/api/v1/meetups",json=meetup,content_type='application/json')
        self.assertEqual(res.status_code,200)
