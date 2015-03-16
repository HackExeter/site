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

'''
class SubmissionRecord(ndb.Model):
    team_name = ndb.StringProperty(indexed=True)
    serve_url = ndb.StringProperty(indexed=False)

class GetUploadUrlHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(blobstore.create_upload_url('/upload'))

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        name = self.request.get('team_name')
        blob = self.get_uploads('file')[0]
        serve_url = '/get_blob/' + blob.key()

        record = SubmissionRecord(
            team_name = name,
            serve_url = serve_url
        )

        record.put()

        self.response.write({
            "success": True
        })

class GetDownloadUrlHandler(webapp2.RequestHandler):
    def get(self):
        name = self.request.get('team_name')
        query = SubmissionRecord.query(SubmissionRecord.team_name == name)
        self.response.write({
            "download_url": query.fetch()[0].serve_url
        })

class DownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        self.send_blob(blobstore.BlobInfo.get(resource))
'''

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

        # Inform the client of success.
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps({
            "records": records
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
    ('/list', ListHandler),
    #('/upload', UploadHandler),
    #('/download', DownloadHandler),
    #('/get_upload_url', GetUploadUrlHandler),
    #('/get_download_url', GetDownloadUrlHandler),
    ('/delete', DeleteHandler)
], debug=True)
