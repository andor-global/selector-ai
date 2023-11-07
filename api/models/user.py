from mongoengine import *
from enum import Enum
import bcrypt


class Sex(Enum):
    Male = "Male"
    Female = "Female"


class MalePsychoType(Enum):
    Classical, Expressive, Spectacular, Natural, Gamine = range(5)


class FemalePsychoType(Enum):
    Classical, Dramatic, Romantic, Natural, Gamine = range(5)


class User(Document):
    email = StringField(unique=True, required=True)
    name = StringField(required=True)
    password = StringField(required=True)
    birth_day = DateField(required=True)
    sex = EnumField(Sex)
    psycho_type = EnumField(enum_types=[MalePsychoType, FemalePsychoType])
    style_goal = StringField()


def hash_password(sender, document):
    if 'password' in document._delta and document._delta['password'][0] != document.password:
        document.password = bcrypt.hashpw(
            document.password.encode('utf-8'), bcrypt.gensalt())


signals.pre_save.connect(hash_password, sender=User)
signals.pre_update.connect(hash_password, sender=User)
