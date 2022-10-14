import aioredis

from datetime import datetime
from urllib.request import Request
from fastapi import FastAPI, Request, status

from schema import VisitedLinks
from utils import extract_domain_from_url

app = FastAPI()
redis = aioredis.from_url("redis://localhost", db=1)
pipeline = redis.pipeline()


@app.post("/visited_links", status_code=status.HTTP_201_CREATED)
async def post_links(links: VisitedLinks):
    cur_time = int(datetime.now().timestamp())
    visited_links = {}
    # extract domains from list of urls and convert into set
    domains = set(map(extract_domain_from_url, links.links))
    # convert set into string and devide it by "*"
    # for add data into redis db
    visited_links[cur_time] = "*".join(domains)
    await pipeline.mset(visited_links)
    await pipeline.execute()
    print(cur_time)
    return {"status": "ok"}


@app.get("/visited_domains", status_code=status.HTTP_200_OK)
async def get_domains(request: Request):
    # template for response
    response = {
        "domains": []
    }
    # get parameters from timestamp and to timestamp 
    # then create a list with integers between these values
    from_timestamp = int(request.query_params["from"])
    to_timestamp = int(request.query_params["to"])
    # get all keys from redis
    redis_keys = await redis.keys()
    # let's go through the list of keys and if it between timestamps
    # add them into the template response
    try:
        for key in redis_keys:
            if int(key) >= from_timestamp and int(key) <= to_timestamp:
                # if key between timestamps get domain from pipeline
                await pipeline.mget(key)
                domains = await pipeline.execute()
                # decode from bytes into string
                domains_string = domains[0][0].decode()
                # split several links by *
                result_domains = domains_string.split("*")
                # go through list of domains and if it does'nt in list of domains
                # append it into response["domains"]
                for domain in result_domains:
                    if domain not in response["domains"]:
                        response["domains"].append(domain)
                response["status"] = "ok"
    except Exception as e:
        response["status"] = str(e)
    return response



