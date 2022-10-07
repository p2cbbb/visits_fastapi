import redis
from datetime import datetime
from urllib.request import Request
from fastapi import FastAPI, Request, status

from app.schema import VisitedLinks
from app.utils import extract_domain_from_url

app = FastAPI()
redis = redis.StrictRedis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)



@app.post("/visited_links", status_code=status.HTTP_201_CREATED)
def post_links(links: VisitedLinks):
    cur_time = int(datetime.now().timestamp())
    visited_links = {}
    # extract domains from list of urls and convert into set
    domains = set(map(extract_domain_from_url, links.links))
    # convert set into string and devide it by "*"
    # for add data into redis db
    visited_links[cur_time] = "*".join(domains)
    redis.mset(visited_links)
    # print(visited_links)
    return {"status": "ok"}


@app.get("/visited_domains", status_code=status.HTTP_200_OK)
def get_domains(request: Request):
    # template for response
    response = {
        "domains": []
    }
    # get parameters from timestamp and to timestamp 
    # then create a list with integers between these values
    from_timestamp = request.query_params["from"]
    to_timestamp = request.query_params["to"]
    range_timestamp = list(range(int(from_timestamp), int(to_timestamp)))
    # let's go through the list of timestamps and if it has domains
    # add them into the template response
    for time_int in range_timestamp:
        try:
            domains = redis.mget(time_int)
            if domains != [None]:
                response["domains"] = domains[0].split("*")
                response["status"] = "ok"
        except Exception as e:
            response["status"] = str(e)
    return response



