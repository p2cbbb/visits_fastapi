from pydantic import BaseModel
from redis_om import HashModel

from config import redis_db


class VisitedLinks(BaseModel):
    links: list

    class Meta:
        database: redis_db