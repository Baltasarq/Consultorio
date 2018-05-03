#!/usr/bin/env python
# MIT License
# (c) baltasar 2016


import webapp2
from google.appengine.api import users
from webapp2_extras import jinja2

from model.appinfo import AppInfo


class MainHandler(webapp2.RequestHandler):
    def get(self):
        user_name = "login"
        user = users.get_current_user()
        if user:
                self.redirect("/main")
                return
        else:
                access_link = users.create_login_url("/main")

        template_values = {
                "user_name": user_name,
                "access_link": access_link,
                "info": AppInfo,
        }

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("index.html", **template_values));

app = webapp2.WSGIApplication([
    ("/", MainHandler),
], debug=True)
