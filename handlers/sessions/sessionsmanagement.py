#!/usr/bin/env python
# MIT License
# (c) baltasar 2016

import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from model.session import Session
from webapp2_extras import jinja2

from model.appinfo import AppInfo
from model.users import User


class SessionsManagementHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        try:
            client_id = self.request.GET['client_id']
        except:
            self.redirect("/error?msg=missing client_id for sessions management")
            return

        if user:
            if User.chk_allowed(user.email()):
                user_name = user.nickname()
                access_link = users.create_logout_url("/")

                try:
                    client = ndb.Key(urlsafe=client_id).get()
                except:
                    self.redirect("/error?msg=client key was not found for sessions management")
                    return

                sessions = Session.query(Session.dni == client.dni).order(-Session.added)

                template_values = {
                    "user_name": user_name,
                    "access_link": access_link,
                    "client": client,
                    "sessions": sessions,
                    "info": AppInfo,
                }

                jinja = jinja2.get_jinja2(app=self.app)
                self.response.write(jinja.render_template("sessionsManagement.html", **template_values))
            else:
                self.redirect("/nouser")
        else:
            self.redirect("/")


app = webapp2.WSGIApplication([
    ("/sessionsManagement", SessionsManagementHandler),
], debug=True)
