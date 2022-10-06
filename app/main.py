import redis
from datetime import datetime
from urllib.request import Request
from fastapi import FastAPI, Request, status
from schema import VisitedLinks
from utils import extract_domain_from_url

app = FastAPI()
redis = redis.StrictRedis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)



@app.post("/visited_links", status_code=status.HTTP_201_CREATED)
def post_links(links: VisitedLinks):
    cur_time = int(datetime.now().timestamp())
    visited_links = {}
    domains = set(map(extract_domain_from_url, links.links))
    visited_links[cur_time] = "*".join(domains)
    redis.mset(visited_links)
    print(visited_links)
    return {"status": "ok"}


@app.get("/visited_domains", status_code=status.HTTP_200_OK)
def get_domains(request: Request):
    response = {
        "domains": []
    }
    from_timestamp = request.query_params["from"]
    to_timestamp = request.query_params["to"]
    range_timestamp = list(range(int(from_timestamp), int(to_timestamp)))
    for t in range_timestamp:
        try:
            domains = redis.mget(t)
            if domains != [None]:
                response["domains"] = domains[0].split("*")
                response["status"] = "ok"
        except Exception as e:
            response["status"] = str(e)
    print(response)
    return response



