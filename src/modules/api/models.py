from datetime import datetime
from typing import List

from pydantic import BaseModel


class CheckRequest(BaseModel):
    ids: List[str]

class PersistItem(BaseModel):
    ts: datetime
    level: str
    message: str
    process: str
    app: str
    extra: dict
    hash: str


class PersistRequest(BaseModel):
    ids: List[PersistItem]
