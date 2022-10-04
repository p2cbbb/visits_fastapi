from redis_om import HashModel
from config import redis_db

class VisitedLinks(HashModel):
    lnks: list

    class Meta:
        database: redis_db