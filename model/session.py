#!/usr/bin/env python
# MIT License
# (c) baltasar 2016

from google.appengine.ext import ndb

class Session(ndb.Model):
    added = ndb.DateProperty(auto_now_add=True, indexed=True)
    dni = ndb.StringProperty(required=True, indexed=True)
    subject = ndb.StringProperty()
    comments = ndb.StringProperty()
    proposal = ndb.StringProperty()
