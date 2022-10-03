from asyncio import current_task
from datetime import datetime
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

class VisitedLinks(BaseModel):
    links: list



@app.post("/visited_links", status_code=status.HTTP_201_CREATED)
async def create_links(links: VisitedLinks):
    cur_time = datetime.now().timestamp()
    print(int(cur_time))
    print(links)
    return {"status": "ok"}



