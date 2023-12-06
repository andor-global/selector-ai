from datetime import datetime
from beanie import Document, Link

from .user import User


class Generation(Document):
    user: Link[User]
    prompt: list[str]
    name: str
    image: str
    created_at: datetime = datetime.utcnow()
