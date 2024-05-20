from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil

from Services import Query,Loading,MySql,URL_Source,File_Source,QStore

app = FastAPI()
procurador = Query()
load = Loading()
db = MySql()
qstore = QStore()

UPLOAD_FOLDER = 'uploads'

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
async def KnowledgeSource(file: UploadFile = File(...), descript: str = Form(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    source = File_Source(file.filename,file_location,file.content_type,descript)
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