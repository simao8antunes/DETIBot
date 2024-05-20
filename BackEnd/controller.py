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
    allow_methods=[""],  # Allows all methods
    allow_headers=["*"]  # Allows all headers
)


@app.get("/detibot")
async def root():
    return "This is the api for DETIBOT"

@app.get("/detibot/url_sources")
async def listUrlSources():
    return db.list_url_sources()

@app.get("/detibot/file_sources")
async def listFileSources():
    return db.list_file_sources()


@app.get("/detibot/{prompt}")
async def Question(prompt: str):
   reposta = procurador.queries(prompt)
   return reposta["query"]



    
@app.post("/detibot/insert_filesource")
async def KnowledgeSourceFile(source: File_Source):
    #inserts the source object into the db
    db.insert_source(source)
    #loads the new source object
    load.file_loader(source)


@app.post("/detibot/insert_urlsource")
async def KnowledgeSourceUrl(source: URL_Source):
    #inserts the source object into the db
    db.insert_source(source)
    #loads the new source object
    load.url_loader(source)

@app.delete("/detibot/delete_urlsource/{id}")
async def deleteUrlSource(id: int):
    db.delete_url_source(id)

@app.delete("/detibot/delete_filesource/{id}")
async def deleteFileSource(id: int):
    db.delete_file_source(id)

@app.put("/detibot/update_urlsource/{id}")
async def updateUrlSource(id: int,source: URL_Source):
    db.update_url_source(id, source)
