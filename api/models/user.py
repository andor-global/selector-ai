from mongoengine import *
from mongoengine import signals
import json
from enum import Enum
from typing import Union
import bcrypt


class Sex(Enum):
    Male = "male"
    Female = "female"


class PsychoType(Enum):
    Classical, Expressive, Dramatic, Spectacular, Romantic, Natural, Gamine = range(
        7)


class User(Document):
    email = StringField(unique=True, required=True)
    name = StringField(required=True)
    password = StringField(required=True)
    birth_day = DateField(required=True)
    sex = EnumField(Sex)
    psycho_type = EnumField(PsychoType)
    style_goal = StringField()


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def hash_password(sender, document):
    if document.password:
        hashed_password = bcrypt.hashpw(
            document.password.encode('utf-8'), bcrypt.gensalt())
        document.password = hashed_password.decode('utf-8')


@signals.pre_save.connect
def user_pre_save(sender, document):
    if isinstance(document, User):
        hash_password(sender, document)
