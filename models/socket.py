import datetime
from mongoengine import *


class Socket(Document):
    sid = StringField(required=True)
    userId = StringField(default='guest')
    is_connected = BooleanField(default=True)
    connected = DateTimeField(default=datetime.datetime.utcnow())
    disconnected = StringField(default="")
