from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Services import *

app = FastAPI()
procurador = Query()
load = Loading()
db = MySql()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can also use [""] to allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"]  # Allows all headers
)


@app.get("/detibot")
async def root():
    return "This is the api for DETIBOT"

@app.get("/detibot/{prompt}")
async def Question(prompt: str):
   reposta = procurador.queries(prompt)
   return reposta["query"]

    

@app.post("/detibot/insert_filesource")
async def KnowledgeSource(source: File_Source):
    #inserts the source object into the db
    db.insert_source(source)
    #loads the new source object
    load.file_loader(source)


@app.post("/detibot/insert_urlsource")
async def KnowledgeSource(source: URL_Source):
    #inserts the source object into the db
    db.insert_source(source)
    #loads the new source object
    load.url_loader(source)