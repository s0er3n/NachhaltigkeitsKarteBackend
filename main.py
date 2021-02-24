from tinydb import TinyDB, Query
from typing import Optional
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
db = TinyDB('db.json')


middleware= [Middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins = ["https://nachhaltigkeitskarte.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)
]

app = FastAPI(middleware=middleware)

class Location(BaseModel):
    name: str
    website: str
    info: str
    category: str
    reason: str
    image: str
    googlemaps: str


@app.get("/")
def main():
  return db.all()

@app.post("/addLocation/")
def addLocation(location: Location):
    data = location.dict()
    data["lat"], data["lon"] = data["googlemaps"].split(
                "@")[1].split(",")[0:2]
    
    data["category"] = [c.strip()
                        for c in data["category"].split(",") if c.strip() != ""]
    data["approved"] = False
    db.insert(data) 
    return location

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info")
