#!/usr/bin/env python
# MIT License
# (c) baltasar 2016

import time

import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras import jinja2

from model.appinfo import AppInfo


class ModifySessionHandler(webapp2.RequestHandler):
    def get(self):
        try:
            id = self.request.GET['session_id']
        except:
            self.redirect("/error?msg=missing session id")
            return

        try:
            client_id = self.request.GET['client_id']
        except:
            self.redirect("/error?msg=missing client id")
            return

        user = users.get_current_user()

        if user:
            user_name = user.nickname()
            access_link = users.create_logout_url("/")

            try:
                session = ndb.Key(urlsafe = id).get()
            except:
                self.redirect("/error?msg=key does not exist modifying session")
                return

            template_values = {
                "info": AppInfo,
                "user_name": user_name,
                "client_id": client_id,
                "access_link": access_link,
                "session": session,
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("modifySession.html", **template_values));
        else:
            self.redirect("/")

    def post(self):
        try:
            client_id = self.request.GET['client_id']
        except:
            self.redirect("/error?msg=missing client id for session modification")
            return

        try:
            session_id = self.request.GET['session_id']
        except:
            self.redirect("/error?msg=missing session id for session modification")
            return

        user = users.get_current_user()

        if user:
            # Get session by key
            try:
                client = ndb.Key(urlsafe=client_id).get()
            except:
                self.redirect("/error?msg=client's key was not found modifying session")
                return

            try:
                session = ndb.Key(urlsafe=session_id).get()
            except:
                self.redirect("/error?msg=session's key does not exist modifying session")
                return

            session.subject = self.request.get("subject", "").strip()
            session.proposal = self.request.get("proposal", "").strip()
            session.comments = self.request.get("comments", "").strip()

            if (len(session.subject) < 1
             or len(session.proposal) < 1):
                self.redirect("/error?msg=Aborted session modification: missing subject or proposal")
                return

            # Save
            session.put()
            time.sleep(1)
            self.redirect("/sessionsManagement?client_id=" + client.key.urlsafe())
        else:
            self.redirect("/")


app = webapp2.WSGIApplication([
    ("/modifySession", ModifySessionHandler),
], debug=True)
