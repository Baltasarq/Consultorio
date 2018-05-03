#!/usr/bin/env python
# MIT License
# (c) baltasar 2015

import webapp2


class Error404Handler(webapp2.RequestHandler):
    def get(self):
        self.redirect("/error?msg=Page was not found.")

app = webapp2.WSGIApplication([
    ("/error404", Error404Handler),
], debug=True)
