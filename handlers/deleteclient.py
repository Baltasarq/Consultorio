#!/usr/bin/env python
# MIT License
# (c) baltasar 2015

import time

import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras import jinja2

from model.appinfo import AppInfo


class DeleteClientHandler(webapp2.RequestHandler):
    def get(self):
        try:
            id = self.request.GET['client_id']
        except:
            id = None

        if not id:
            self.redirect("/error?msg=serie was not found")
            return

        user = users.get_current_user()

        if user:
            user_name = user.nickname()
            access_link = users.create_logout_url("/")

            try:
                client = ndb.Key(urlsafe=id).get()
            except:
                self.redirect("/error?msg=client key was not found")
                return

            template_values = {
                "info": AppInfo,
                "user_name": user_name,
                "access_link": access_link,
                "client": client,
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("deleteClient.html", **template_values));
        else:
            self.redirect("/")

    def post(self):
        try:
            id = self.request.GET['client_id']
        except:
            id = None

        if id == None:
            self.redirect("/error?msg=id missing for deletion")
            return

        user = users.get_current_user()

        if (user
        and id):
            try:
                client = ndb.Key(urlsafe = id).get()
            except:
                self.redirect("/error?msg=key was not found")
                return

            client.key.delete();
            time.sleep(1)
            self.redirect("/main")
        else:
            self.redirect("/")

app = webapp2.WSGIApplication([
    ("/deleteClient", DeleteClientHandler),
], debug=True)
