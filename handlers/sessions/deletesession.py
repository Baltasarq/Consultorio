#!/usr/bin/env python
# MIT License
# (c) baltasar 2015

import time

import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras import jinja2

from model.appinfo import AppInfo


class DeleteSessionHandler(webapp2.RequestHandler):
    def get(self):
        try:
            id = self.request.GET['session_id']
        except:
            self.redirect("/error?msg=session key was not found deleting session")
            return

        try:
            client_id = self.request.GET['client_id']
        except:
            self.redirect("/error?msg=client key was not found deleting session")
            return

        user = users.get_current_user()

        if user:
            user_name = user.nickname()
            access_link = users.create_logout_url("/")

            try:
                session = ndb.Key(urlsafe=id).get()
            except:
                self.redirect("/error?msg=session key was not found deleting session (get)")
                return

            try:
                client = ndb.Key(urlsafe=client_id).get()
            except:
                self.redirect("/error?msg=client key was not found deleting session (get)")
                return

            template_values = {
                "info": AppInfo,
                "user_name": user_name,
                "access_link": access_link,
                "session": session,
                "client": client,
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("deleteSession.html", **template_values));
        else:
            self.redirect("/")

    def post(self):
        try:
            client_id = self.request.GET['client_id']
        except:
            self.redirect("/error?msg=client was not found")
            return

        try:
            id = self.request.GET['session_id']
        except:
            self.redirect("/error?msg=id missing for deletion")
            return

        user = users.get_current_user()

        if (user
        and id):
            try:
                session = ndb.Key(urlsafe = id).get()
            except:
                self.redirect("/error?msg=key was not found deleting session (post)")
                return

            try:
                client = ndb.Key(urlsafe = client_id).get()
            except:
                self.redirect("/error?msg=client key was not found deleting session (post)")
                return

            session.key.delete();
            time.sleep(1)
            self.redirect("/sessionsManagement?client_id=" + client.key.urlsafe())
        else:
            self.redirect("/")

app = webapp2.WSGIApplication([
    ("/deleteSession", DeleteSessionHandler),
], debug=True)
