from google.appengine.ext import ndb

class TaskManager(ndb.Model):
    besedilo = ndb.StringProperty()
    rok = ndb.StringProperty()
    nastanek = ndb.DateTimeProperty(auto_now_add=True)
    narejeno = ndb.BooleanProperty(default=False)
    izbrisano = ndb.BooleanProperty(default=False)