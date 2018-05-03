#!/usr/bin/env python
# MIT License
# (c) baltasar 2015

import datetime
import time

import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras import jinja2

from model.client import Client
from model.appinfo import AppInfo


class ModifyClientHandler(webapp2.RequestHandler):
    def get(self):
        try:
            id = self.request.GET['client_id']
        except:
            self.redirect("/error?msg=client was not found")
            return

        user = users.get_current_user()

        if user:
            user_name = user.nickname()
            access_link = users.create_logout_url("/")

            try:
                client = ndb.Key(urlsafe = id).get()
            except:
                self.redirect("/error?msg=key does not exist")
                return

            template_values = {
                "info": AppInfo,
                "user_name": user_name,
                "access_link": access_link,
                "client": client,
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("modifyClient.html", **template_values));
        else:
            self.redirect("/")

    def post(self):
        try:
            id = self.request.GET['client_id']
        except:
            id = None

        if not id:
            self.redirect("/error?msg=missing id for modification")
            return

        user = users.get_current_user()
        client = None

        if user:
            # Get client by key
            try:
                client = ndb.Key(urlsafe = id).get()
            except:
                self.redirect("/error?msg=key does not exist")
                return

            zip = 0
            try:
                zip = int(self.request.get("zip", 0))
            except:
                pass

            txtBirth = self.request.get("birth", datetime.date.today().isoformat())
            birth = datetime.datetime.strptime(txtBirth, "%Y-%m-%d")

            client.dni = self.request.get("dni", "").strip()
            client.name = self.request.get("name", "").strip()
            client.surname = self.request.get("surname", "").strip()
            client.address = self.request.get("address", "").strip()
            client.city = self.request.get("city", "").strip()
            client.zip = zip
            client.birth = birth
            client.email = self.request.get("email", "").strip()
            client.phone = self.request.get("phone", "").strip()
            client.comments = self.request.get("comments", "").strip()

            # Chk
            if zip < 1:
                self.redirect("/error?msg=Aborted modification: invalid dni")
                return

            if (len(client.surname) < 1
             or len(client.name) < 1):
                self.redirect("/error?msg=Aborted modification: missing name and surname")
                return

            # Chk dni
            existingClients = Client.query(Client.dni == client.dni)
            if  (existingClients
             and existingClients.count() > 0
             and existingClients.get() != client):
                self.redirect("/error?msg=Cliente con dni: " + client.dni + " ya existe.")
                return

            # Chk surname
            existingClients = Client.query(Client.surname == client.surname).filter(Client.name == client.name)
            if (existingClients
            and existingClients.count() > 0
            and existingClients.get() != client):
                self.redirect("/error?msg=Cliente con apellidos y nombre: " + client.surname + ", " + client.name +  " ya existe.")
                return


            # Save
            client.put()
            time.sleep(1)
            self.redirect("/main")
        else:
            self.redirect("/")

app = webapp2.WSGIApplication([
    ("/modifyClient", ModifyClientHandler),
], debug=True)
