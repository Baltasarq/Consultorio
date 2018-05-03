#!/usr/bin/env python
# MIT License
# (c) baltasar 2016


import time
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras import jinja2

from model.appinfo import AppInfo
from model.users import User

class AdminHandler(webapp2.RequestHandler):
    def get(self):
        users = User.query()

        template_values = {
            "users": users,
            "info": AppInfo,
        }

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("admin.html", **template_values))

    def post(self):
        email = self.request.get("edEmail", "")
        name = self.request.get("edName", "")
        address = self.request.get("edAddress", "")
        phone = self.request.get("edPhone", "")
        operation = self.request.get("edOp", "")

        if email and operation:
            if operation == "add":
                user = User()
                user.email = email
                user.name = name
                user.address = address
                user.phone = phone
                user.put()
                time.sleep(1)
            elif operation == "delete":
                user = User.query(User.email == email)
                if user:
                    user = user.get()
                    user.key.delete()
                    time.sleep(1)
                else:
                    self.redirect("/error?msg=user was not found")
            self.redirect("/admin")
        else:
            self.redirect("/error?msg=email and operation needed")

        return


app = webapp2.WSGIApplication([
    ("/admin", AdminHandler),
], debug=True)
