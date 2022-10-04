import aioredis
import datetime as dt
from fastapi import FastAPI, status
from schema import VisitedLinks

app = FastAPI()
redis = aioredis.from_url('redis://localhost:6379', encoding='utf-8', decode_responses=True)


@app.post("/visited_links", status_code=status.HTTP_201_CREATED)
async def create_links(links: VisitedLinks):
    cur_time = dt.now().timestamp()
    print(int(cur_time))
    print(links)
    links.save()
    await redis.set('links', cur_time, links)
    # links.time = int(cur_time)
    return {"status": "ok"}



