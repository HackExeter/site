import webapp2
import json
import datetime

from google.appengine.ext import ndb
from google.appengine.ext import blobstore

# Record
# A record of a single signup (database entry).
class Record(ndb.Model):
    name = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)
    organisation = ndb.StringProperty(indexed=False)
    members = ndb.StringProperty(repeated=True)
    timestamp = ndb.DateTimeProperty(auto_now_add=True)

# InterestedRecord
# A record of a pre-signup interest thing
class InterestedRecord(ndb.Model):
    email = ndb.StringProperty(indexed=False)

# RegistrationHandler
# The handler that listens on /register
# for signup submissions
class RegistrationHandler(webapp2.RequestHandler):
    def get(self):

        # Create and insert a record
        # for this registration.
        record = Record(parent=ndb.Key('Records', 'default'))

        record.name = self.request.get('name')
        record.email = self.request.get('email')
        record.organisation = self.request.get('organisation')
        record.members = json.loads(self.request.get('members'))

        record.put()

        # Inform the client of success.
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps({
            'success': True
        }))

# InterestedHandler
# Handler that listens on /interested
# for pre-registration interest submissions
class InterestedHandler(webapp2.RequestHandler):
    def get(self):

        # Create and insert a record
        # for this registration.
        record = InterestedRecord(parent=ndb.Key('Interested', 'default'))
        record.email = self.request.get('email')
        record.put()

        # Inform the client of success.
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps({
            'success': True
        }))

class ListHandler(webapp2.RequestHandler):
    def get(self):
        query = Record.query(Record.timestamp > datetime.datetime(2015, 1, 1))
        records = []
        for record in query:
            records.append({
                "id": record.key.id(),
                "name": record.name,
                "email": record.email,
                "members": record.members,
                "organisation": record.organisation,
                "timestamp": record.timestamp.strftime("%s")
            })

        query = InterestedRecord.query()
        interested = []

        for record in query:
            interested.append(record.email)

        # Inform the client of success.
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps({
            "records": records,
            "interested": interested
        }))

class DeleteHandler(webapp2.RequestHandler):
    def get(self):
        success = False
        record = Record.get_by_id(int(self.request.get('id')), parent=ndb.Key('Records', 'default'))
        if record is not None:
            record.key.delete()
            success = True
        else:
            success = False

        # Inform the client of success.
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps({
            'success': success
        }))

application = webapp2.WSGIApplication([
    ('/register', RegistrationHandler),
    ('/interested', InterestedHandler),
    ('/list', ListHandler),
    ('/delete', DeleteHandler)
], debug=True)
