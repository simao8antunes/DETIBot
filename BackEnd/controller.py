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
UPLOAD_FOLDER = "./uploads"

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
async def SourceFile(file: UploadFile = File(...), descript: str = Form(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    print(file.content_type)
    source = File_Source(file_name=file.filename,file_path=file_location,loader_type=file.content_type,description=descript)
    #inserts the source object into the db
    db.insert_source(source)
    #loads the new source object
    load.file_loader(source)


@app.post("/detibot/insert_urlsource")
async def SourceUrl(source: URL_Source):
    print(source)
    #inserts the source object into the db
    db.insert_source(source)
    #loads the new source object
    load.url_loader(source)

@app.delete("/detibot/delete_urlsource/{id}")
async def deleteUrlSource(id: int):
    current_source = db.get("SELECT file_path FROM file_source WHERE id = %s",[id])
    qstore.delete_vectors(current_source[0])
    db.delete_url_source(id)

@app.delete("/detibot/delete_filesource/{id}")
async def deleteFileSource(id: int):
    current_source = db.get("SELECT url_link FROM url_source WHERE id = %s",[id])
    qstore.delete_vectors(current_source[0])
    db.delete_file_source(id)


@app.put("/detibot/update_urlsource/{id}")
async def updateUrlSource(id: int,source: URL_Source):
    db.update_url_source(id, source)
    load.url_loader(source)

@app.put("/detibot/update_filesource/{id}")
async def updateFileSource(id: int,file: UploadFile = File(...), descript: str = Form(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    current_source = db.get("SELECT file_path FROM file_source WHERE id = %s",[id])
    if not current_source:
        raise HTTPException(status_code=404, detail="File source not found")

    if os.path.exists(current_source[0]):
        os.remove(current_source[0])
    
    new_file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(new_file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    updated_source = File_Source(file.filename, new_file_location, file.content_type, descript)
    db.update_file_source(id, updated_source)
    load.file_loader(updated_source)
