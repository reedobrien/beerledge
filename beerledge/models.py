import os
from datetime import datetime
from hashlib import sha256
import hmac
from urlparse import urlparse

from pyramid.settings import get_settings

from mongoengine import connect, Document, StringField, EmailField, DateTimeField, ListField, BooleanField


class User(Document):
    username = StringField(required=True, unique=True)
    email = EmailField(required=True)
    passhash = StringField(required=True)
    groups = ListField(default=['group:user', ])
    disabled = BooleanField(default=False)
    created = DateTimeField(default=datetime.utcnow())

    meta = {
        'ordering': ['-created']
    }

    def get_userid(self):
        return self._id

    def set_password(self, password):
        settings = get_settings()
        return hmac.new(settings['secret'], password, sha256).hexdigest()

    def check_password(self, password):
        settings = get_settings()
        return self.passhash == hmac.new(settings['secret'], password, sha256).hexdigest()


class Checkin(Document):
    beer = StringField(required=True)
    checkin_place = StringField(required=True)
    username = StringField(required=True)
    created = DateTimeField(default=datetime.utcnow())

    meta = {
        'ordering': ['-created']
    }


def add_mongo(event):
    req = event.request
    database = urlparse(os.environ.get('MONGOHQ_URL', 'mongodb://127.0.0.1:27017/beerledge'))
    req.db = connect(database.path[1:],
                     host=database.hostname,
                     port=database.port,
                     username=database.username,
                     password=database.password)
