
import redis
from datetime import datetime
from urllib.request import Request
from fastapi import FastAPI, Request, status
from schema import VisitedLinks

app = FastAPI()
redis = redis.StrictRedis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)
# redis = aioredis.from_url('redis://localhost:6379', encoding='utf-8', decode_responses=True)


@app.get('/')
async def Home():
    return "Welcome Home"


@app.post("/visited_links", status_code=status.HTTP_201_CREATED)
def post_links(links: VisitedLinks):
    cur_time = int(datetime.now().timestamp())
    visited_links = {}
    # for link in links.links:
    #     domains.add(link)
    #     visited_links[cur_time] = link
    #     print(link)
    visited_links[cur_time] = str(links.links)
    redis.mset(visited_links)
    print(visited_links)
    return {"status": "ok"}


@app.get("/visited_domains", status_code=status.HTTP_200_OK)
def get_domains(request: Request):
    from_timestamp = request.query_params["from"]
    to_timestamp = request.query_params["to"]
    range_timestamp = list(range(int(from_timestamp), int(to_timestamp)))
    # print(range_timestamp)
    for t in range_timestamp:
        try:
            res = redis.mget(t)
            if res != [None]:
                print(res)
        except Exception as e:
            continue
    # result = redis.mget('')
    # print(result)
    return {"from": from_timestamp, "to": to_timestamp}



