#!/usr/bin/env python
# MIT License
# (c) baltasar 2016

import datetime

import webapp2
from google.appengine.api import users

from model.client import Client


class AddClientHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        num_clients = Client.query().count()

        if user:
            client = Client()
            client.user = user.user_id()
            client.dni = str(num_clients);
            client.name = "Juan"
            client.surname = "Nadie Nadie";
            client.address = "Percebe, 13"
            client.zip = 123
            client.city = "Ys"
            client.birth = datetime.date.today() - datetime.timedelta(days=(20*365.24))
            client.phone = "";
            client.email = "";
            client.comments = "";
            key = client.put()
            self.redirect("/modifyClient?client_id=" + key.urlsafe())
        else:
            self.redirect("/")

        return

app = webapp2.WSGIApplication([
    ("/addClient", AddClientHandler),
], debug=True)
