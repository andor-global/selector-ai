from datetime import datetime
from enum import Enum, auto
from beanie import Document, Indexed


class Sex(str, Enum):
    Male = "male"
    Female = "female"


class PsychoType(Enum):
    Classical = auto()
    Expressive = auto()
    Dramatic = auto()
    Spectacular = auto()
    Romantic = auto()
    Natural = auto()
    Gamine = auto()


class User(Document):
    email: Indexed(str, unique=True)
    name: str
    password: str
    birth_day: datetime
    sex: Sex
    psycho_type: PsychoType

    def get_age(self) -> int:
        today = datetime.utcnow()
        age = today.year - self.birth_day.year - ((today.month, today.day) < (self.birth_day.month, self.birth_day.day))
        return age
