import datetime
from mongoengine import *


class User(Document):
    name = StringField(required=True)
    phoneNumber = StringField(default='guest')
    token = StringField(default="")
    friends = ListField(default=[])
