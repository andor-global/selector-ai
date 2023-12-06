from datetime import datetime
from enum import Enum, auto
import json
import os
from pathlib import Path
from typing import Optional
from beanie import Document, Indexed


class Sex(str, Enum):
    Male = "male"
    Female = "female"


class PsychoType(str, Enum):
    Classical = "classical"
    Expressive = "expressive"
    Dramatic = "dramatic"
    Spectacular = "spectacular"
    Romantic = "romantic"
    Natural = "natural"
    Gamine = "gamine"


class User(Document):
    email: Indexed(str, unique=True)
    name: str
    password: str
    birth_day: datetime
    sex: Sex
    psycho_type: Optional[str] = ''

    def get_age(self) -> int:
        today = datetime.utcnow()
        age = today.year - self.birth_day.year - ((today.month, today.day) < (self.birth_day.month, self.birth_day.day))
        return age

    def get_psychotype_info(self) -> dict:
        path = Path(__file__).resolve().parent / Path("../../psychotype/psychotypes.json")
        with open(path, 'r') as file:
            data = json.load(file)
            return data[self.sex][self.psycho_type]
