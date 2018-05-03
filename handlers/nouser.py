#!/usr/bin/env python
# MIT License
# (c) baltasar 2016


import webapp2
from model.appinfo import AppInfo
from webapp2_extras import jinja2
from google.appengine.api import users


class NoUserHandler(webapp2.RequestHandler):
    def get(self):
        access_link = users.create_logout_url("/")
        user = users.get_current_user()

        if user:
            user_name = user.nickname()
        else:
            user_name = "logout"

        template_values = {
            "info": AppInfo,
            "access_link": access_link,
            "user_name": user_name,
        }

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("nouser.html", **template_values))



app = webapp2.WSGIApplication([
    ("/nouser", NoUserHandler),
], debug=True)
