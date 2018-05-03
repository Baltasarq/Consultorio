#!/usr/bin/env python
# MIT License
# (c) baltasar 2016

from google.appengine.ext import ndb

class Client(ndb.Model):
    added = ndb.DateProperty(auto_now_add=True)
    user = ndb.StringProperty(required=True, indexed=True)
    dni = ndb.StringProperty(required=True, indexed=True)
    name = ndb.StringProperty(required=True, indexed=True)
    surname = ndb.StringProperty(required=True, indexed=True)
    address = ndb.StringProperty(required=True)
    city = ndb.StringProperty(required=True)
    zip = ndb.IntegerProperty(required=True)
    birth = ndb.DateProperty()
    phone = ndb.StringProperty()
    email = ndb.StringProperty()
    comments = ndb.StringProperty()
