#!/usr/bin/env python
# MIT License
# (c) baltasar 2016

import webapp2
from model.client import Client
from google.appengine.api import users
from webapp2_extras import jinja2

from model.appinfo import AppInfo
from model.users import User


class ClientsManagementHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            if User.chk_allowed(user.email()):
                user_name = user.nickname()
                access_link = users.create_logout_url("/")
                clients = Client.query().order(Client.surname)

                template_values = {
                    "info": AppInfo,
                    "user_name": user_name,
                    "access_link": access_link,
                    "clients": clients,
                }

                jinja = jinja2.get_jinja2(app=self.app)
                self.response.write(jinja.render_template("clientsManagement.html", **template_values))
            else:
                self.redirect("/nouser")
        else:
            self.redirect("/")

    def post(self):
        user = users.get_current_user()

        if not user:
            self.redirect("/")
            return

        key_text = self.request.get("lookFor", None)
        dni_text = self.request.get("lookForDni", None)

        if not key_text and not dni_text:
            self.redirect("/main")
            return

        if dni_text:
            dni_text = dni_text.strip()
            try:
                dni = int(dni_text)
            except:
                dni = 0

            key_text = dni_text
            self.result_set = Client.query(Client.dni == dni).order(Client.surname)
        else:
            self.key_text = key_text.strip().lower()
            self.result_set = []
            Client.query().order(Client.surname).map(self.key_text)

        template_values = {
            "info": AppInfo,
            "user_name": user.nickname(),
            "access_link": users.create_logout_url("/"),
            "clients": self.result_set,
            "key_text": key_text
        }

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("found.html", **template_values))

    def lookFor(self, client):
        surname = client.surname.lower()
        name = client.name.lower()

        if (self.key_text in surname
         or self.key_text in name):
            self.result_set += [client]

        return


app = webapp2.WSGIApplication([
    ("/main", ClientsManagementHandler),
], debug=True)
