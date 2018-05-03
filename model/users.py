#!/usr/bin/env python
# MIT License
# (c) baltasar 2016

from google.appengine.ext import ndb
from google.appengine.api import users


class User(ndb.Model):
    added = ndb.DateProperty(auto_now_add=True)
    email = ndb.StringProperty(required=True, indexed=True)
    name = ndb.StringProperty(required=True)
    address = ndb.StringProperty()
    phone = ndb.StringProperty()

    @staticmethod
    def chk_allowed(user_email):
        toret = users.is_current_user_admin()

        if not(toret):
            try:
                toret = User.query(User.email == user_email).count() > 0
            except:
                toret = False

        return toret
