from fastapi import FastAPI
from Services import *

app = FastAPI()
query = Query()
load = Loading()
db = H2()



@app.get("/detibot")
async def root():
    return "This is the api for DETIBOT"

@app.get("/detibot/{prompt}")
async def Question(prompt: str):
   return  query.queries(prompt)
    

@app.post("/detibot/insert_source")
async def KnowledgeSource(source: Source):
    #inserts the source object into the db
    db.insert_source(source)
    #loads the new source object
    load.loader()