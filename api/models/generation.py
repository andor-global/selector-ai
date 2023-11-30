from datetime import datetime
from beanie import Document, Indexed
from beanie.operators import File


class Generation(Document):
    user: Link[User]
    prompt: list[str]
    name: str
    image: File
    created_at: datetime = datetime.utcnow()
