import redis
from datetime import datetime
from urllib.request import Request
from fastapi import FastAPI, Request, status

from schema import VisitedLinks
from utils import extract_domain_from_url

app = FastAPI()
redis = redis.StrictRedis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)
pipeline = redis.pipeline()


@app.post("/visited_links", status_code=status.HTTP_201_CREATED)
def post_links(links: VisitedLinks):
    cur_time = int(datetime.now().timestamp())
    visited_links = {}
    # extract domains from list of urls and convert into set
    domains = set(map(extract_domain_from_url, links.links))
    # convert set into string and devide it by "*"
    # for add data into redis db
    visited_links[cur_time] = "*".join(domains)
    pipeline.mset(visited_links)
    pipeline.execute()
    print(cur_time)
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
    redis_keys = redis.keys()
    # let's go through the list of keys and if it between timestamps
    # add them into the template response
    try:
        for key in redis_keys:
            if key >= from_timestamp and key <= to_timestamp:
                pipeline.mget(key)
                domains = pipeline.execute()[0]
                result_domains = domains[0].split("*")
                response["domains"] = result_domains
                response["status"] = "ok"
    except Exception as e:
        response["status"] = str(e)
    return response



