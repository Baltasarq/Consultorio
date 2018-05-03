#!/usr/bin/env python
# MIT License
# (c) baltasar 2016

import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras import jinja2

from model.appinfo import AppInfo
from model.users import User


class ReportSessionHandler(webapp2.RequestHandler):
    def get(self):
        try:
            session_id = self.request.GET['session_id']
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
            if User.chk_allowed(user.email()):
                try:
                    session = ndb.Key(urlsafe=session_id).get()
                except:
                    self.redirect("/error?msg=key does not exist for session creating report")
                    return

                try:
                    user_info = User.query(User.email == user.email()).get()
                except:
                    self.redirect("/error?msg=user info was not found")
                    return

                try:
                    client = ndb.Key(urlsafe=client_id).get()
                except:
                    self.redirect("/error?msg=key does not exist for client creating report for session")
                    return

                template_values = {
                    "user_info": user_info,
                    "info": AppInfo,
                    "client": client,
                    "session": session,
                }

                jinja = jinja2.get_jinja2(app=self.app)
                self.response.write(jinja.render_template("reportSession.html", **template_values));
            else:
                self.redirect("/nouser")
        else:
            self.redirect("/")


app = webapp2.WSGIApplication([
    ("/reportSession", ReportSessionHandler),
], debug=True)
