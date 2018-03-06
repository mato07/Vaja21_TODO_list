#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import TaskManager


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("main.html")

class RezultatHandler(BaseHandler):
    def post(self):
        naloga = self.request.get("vpisano")
        dan = self.request.get("dan")
        mesec = self.request.get("mesec")
        leto = self.request.get("leto")
        datum = dan + "."+ mesec + "." + leto
        nalogica = TaskManager(besedilo=naloga, rok=datum)
        nalogica.put()
        return self.render_template("rezultat.html")

class ListHandler(BaseHandler):
    def get(self):
        seznam_neopr = TaskManager.query(TaskManager.izbrisano == False, TaskManager.narejeno == False).fetch()
        podatki = {"seznam_neopr": seznam_neopr}
        return self.render_template("seznam_neopr.html", podatki)

class PosameznaNalogaHandler(BaseHandler):
    def get(self, vnos_id):
        sporocilce = TaskManager.get_by_id(int(vnos_id))
        params = {"posamezno_sporocilce": sporocilce}
        return self.render_template("posamezna_naloga.html", params=params)

class UrediHandler(BaseHandler):
    def get(self, vnos_id):
        sporocilce = TaskManager.get_by_id(int(vnos_id))
        params = {"posamezno_sporocilce": sporocilce}
        return self.render_template("uredi.html", params=params)

    def post(self, vnos_id):
        sporocilce = TaskManager.get_by_id(int(vnos_id))
        sporocilce.besedilo = self.request.get("novo-besedilo")
        sporocilce.rok = self.request.get("nov-rok")
        sporocilce.put()
        return self.redirect_to("seznam-neopravljenih")

class OpraviHandler(BaseHandler):
    def get(self, vnos_id):
        sporocilce = TaskManager.get_by_id(int(vnos_id))
        params = {"posamezno_sporocilce": sporocilce}
        return self.render_template("opravljeno.html", params=params)

    def post(self, vnos_id):
        sporocilce = TaskManager.get_by_id(int(vnos_id))
        sporocilce.narejeno = True
        sporocilce.put()
        return self.redirect_to("seznam-opravljenih")

class IzbrisiHandler(BaseHandler):
    def get(self, vnos_id):
        sporocilce = TaskManager.get_by_id(int(vnos_id))
        params = {"posamezno_sporocilce": sporocilce}
        return self.render_template("izbrisano.html", params=params)

    def post(self, vnos_id):
        sporocilce = TaskManager.get_by_id(int(vnos_id))
        sporocilce.izbrisano = True
        sporocilce.put()
        return self.redirect_to("seznam-neopravljenih")

class List2Handler(BaseHandler):
    def get(self):
        seznam_opr = TaskManager.query(TaskManager.izbrisano == False, TaskManager.narejeno == True).fetch()
        podatki = {"seznam_opr": seznam_opr}
        return self.render_template("seznam_opr.html", podatki)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/rezultat', RezultatHandler),
    webapp2.Route('/seznam_neopravljenih', ListHandler, name="seznam-neopravljenih"),
    webapp2.Route('/naloga/<vnos_id:\d+>', PosameznaNalogaHandler),
    webapp2.Route('/naloga/<vnos_id:\d+>/uredi', UrediHandler),
    webapp2.Route('/naloga/<vnos_id:\d+>/opravljeno', OpraviHandler),
    webapp2.Route('/naloga/<vnos_id:\d+>/izbrisano', IzbrisiHandler),
    webapp2.Route('/seznam_opravljenih', List2Handler, name="seznam-opravljenih"),
], debug=True)
