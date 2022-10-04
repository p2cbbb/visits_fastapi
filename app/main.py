import aioredis
from datetime import datetime
from fastapi import FastAPI, status
from schema import VisitedLinks

app = FastAPI()
redis = aioredis.from_url('redis://localhost:6379', encoding='utf-8', decode_responses=True)


@app.get('/')
async def Home():
    return "Welcome Home"


@app.post("/visited_links", status_code=status.HTTP_201_CREATED)
async def create_links(links: VisitedLinks):
    cur_time = int(datetime.now().timestamp())
    print(cur_time)
    print(links)
    await redis.set('links', f"{str(links)}:{str(cur_time)}")
    result = await redis.get('links')
    print(result)
    return {"status": "ok"}


