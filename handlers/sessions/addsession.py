#!/usr/bin/env python
# encoding: utf-8
# MIT License
# (c) baltasar 2016

import webapp2
from google.appengine.ext import ndb

from model.session import Session


class AddSessionHandler(webapp2.RequestHandler):
    def get(self):
        try:
            client_id = self.request.GET['client_id']
        except:
            self.redirect("/error?msg=missing client_id for new session")
            return

        try:
            client = ndb.Key(urlsafe=client_id).get()
        except:
            self.redirect("/error?msg=client was not found")
            return

        session = Session()
        session.dni = client.dni
        session.subject = "Revisión"
        session.comments = ""
        session.proposal = ""
        session.put()
        self.redirect("/modifySession?session_id=" + session.key.urlsafe() + "&client_id=" + client_id)


app = webapp2.WSGIApplication([
    ("/addSession", AddSessionHandler),
], debug=True)
