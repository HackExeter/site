import webapp2
import json
import datetime
import time

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

class MentorRecord(ndb.Model):
    name = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)
    languages = ndb.StringProperty(indexed=False)
    experience = ndb.StringProperty(indexed=False)
    timestamp = ndb.DateTimeProperty(auto_now_add=True)

class TeamScoreRecord(ndb.Model):
    number = ndb.IntegerProperty(indexed=True)
    email = ndb.StringProperty(indexed=False)
    members = ndb.StringProperty(repeated=True, indexed=False)
    notes = ndb.StringProperty(repeated=True, indexed=False)
    scores = ndb.StringProperty(repeated=True, indexed=False)

class GetScoreTeamsHandler(webapp2.RequestHandler):
    def get(self):
        query = TeamScoreRecord.query()
        teams = []
        for team in query:
            teams.append({
                'number': team.number,
                'members': team.members
            })
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps({
            'teams': teams
        }))

class CreateScoreTeamHandler(webapp2.RequestHandler):
    def get(self):
        # Create and insert a record
        # for this registration.
        record = TeamScoreRecord()

        record.number = int(self.request.get('number'))
        record.members = json.loads(self.request.get('members'))
        record.notes = []
        record.scores = []

        record.put()

        # Inform the client of success.
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps({
            'success': True
        }))

class AddNoteHandler(webapp2.RequestHandler):
    def get(self):
        record = TeamScoreRecord.query(TeamScoreRecord.number == int(self.request.get('team_number'))).fetch()
        if len(record) > 0:
            record = record[0]
            record.notes.append(json.dumps({
                'note': self.request.get('note'),
                'timestamp': time.time()
            }))
            record.put()

            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps({
                'success': True,
                'notes': json.dumps(map((lambda x: json.loads(x)), record.notes))
            }))
        else:
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps({
                'success': True
            }))

class AddScoreHandler(webapp2.RequestHandler):
    def get(self):
        record = TeamScoreRecord.query(TeamScoreRecord.number == int(self.request.get('team_number')))
        record.scores.append(json.dumps({
            'score': json.loads(self.request.get('score')),
            'judge': self.request.get('judge'),
            'timestamp': datetime.now()
        }))
        record.put()

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps({
            'success': True,
            'scores': json.dumps(map(record.scores, lambda x: json.loads(x)))
        }))

class GetScoresHandler(webapp2.RequestHandler):
    def get(self):
        record = TeamScoreRecord.query(TeamScoreRecord.number == int(self.request.get('team_number'))).fetch()

        if len(record) > 0:
            record = record[0]

            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps({
                'success': True,
                'members': record.members,
                'notes': map((lambda x: json.loads(x)), record.notes),
                'scores': map((lambda x: json.loads(x)), record.scores),
            }))
        else:
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps({
                'success': False
            }))

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

class RegisterMentorHandler(webapp2.RequestHandler):
    def get(self):

        # Create and insert a record
        # for this registration.
        record = MentorRecord(parent=ndb.Key('MentorRecords', 'default'))

        record.name = self.request.get('name')
        record.email = self.request.get('email')
        record.size = self.request.get('size')
        record.languages = self.request.get('languages')
        record.experience = self.request.get('experience')

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
        query = Record.query(Record.timestamp > datetime.datetime(2015, 3, 1))
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
    ('/register_mentor', RegisterMentorHandler),
    ('/interested', InterestedHandler),
    ('/list', ListHandler),
    ('/delete', DeleteHandler),
    ('/list_score_teams', GetScoreTeamsHandler),
    ('/create_score_team', CreateScoreTeamHandler),
    ('/add_note', AddNoteHandler),
    ('/get_score', GetScoresHandler)
], debug=True)
