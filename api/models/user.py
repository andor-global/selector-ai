from mongoengine import *
from mongoengine import signals
from datetime import datetime
from enum import Enum
from bson import ObjectId
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

    def get_age(self) -> int:
        today = datetime.utcnow()
        age = today.year - self.birth_day.year - ((today.month, today.day) < (self.birth_day.month, self.birth_day.day))
        return age

    @staticmethod
    def get_user_by_id(id: str):
        return User.objects.exclude('password').get(id=ObjectId(id))


def hash_password(sender, document):
    if document.password:
        hashed_password = bcrypt.hashpw(
            document.password.encode('utf-8'), bcrypt.gensalt())
        document.password = hashed_password.decode('utf-8')


@signals.pre_save.connect
def user_pre_save(sender, document):
    if isinstance(document, User):
        hash_password(sender, document)
