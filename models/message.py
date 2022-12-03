import datetime
from mongoengine import *


class Message(Document):
    f = StringField(required=True)
    t = StringField(required=True)  # Person, group or channel id
    content = StringField(required=True)
    has_multimedia = BooleanField(default=False)
    multimedia = StringField(default="")
    type = StringField(default="person")  # Can be group or channel
    cencored = BooleanField(default=False)
    created = DateTimeField(default=datetime.datetime.utcnow())
