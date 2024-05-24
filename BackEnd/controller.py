from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil

from Services import Query,Loading,MySql,URL_Source,File_Source,QStore,Faq_Source


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
#---------------------- endpoints that returns an answer given a prompt--------------------------- 
@app.get("/detibot/en/{prompt}")
async def QuestionEn(prompt: str):
   reposta = procurador.queries(prompt,"en")
   return reposta["query"]

@app.get("/detibot/pt/{prompt}")
async def QuestionPt(prompt: str):
   reposta = procurador.queries(prompt,"pt")
   return reposta["query"]

#-------------------------enpoints that list every row of a table in mysql--------------------------
@app.get("/detibot/url_sources")
async def listUrlSources():
    return db.list_url_sources()

@app.get("/detibot/file_sources")
async def listFileSources():
    return db.list_file_sources()

@app.get("/detibot/faq_sources")
async def listFaqSources():
    return db.list_faq_sources()

#------------------------ endpoints to apply a search bar in each table of sources-------------------
@app.get("/detibot/Search_url_sources/{search}")
async def searchUrlSources(search:str):
    return db.search_url_sources()

@app.get("/detibot/Search_file_sources/{search}")
async def searchFileSources(search:str):
    return db.search_file_sources()

@app.get("/detibot/Search_faq_sources/{search}")
async def searchFaqSources(search:str):
    return db.search_faq_sources()
#------------------------ endpoints that post the diferent type of sources in the system-----------------

@app.post("/detibot/insert_filesource")
async def SourceFile(file: UploadFile = File(...), descript: str = Form(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    source = File_Source(file_name=file.filename,file_path=file_location,loader_type=file.content_type,description=descript)
    #inserts the source object into the db
    db.insert_source(source)
    #loads the new source object
    load.file_loader(source)

@app.post("/detibot/insert_urlsource")
async def SourceUrl(source: URL_Source):
    #inserts the source object into the db
    db.insert_source(source)
    #loads the new source object
    load.url_loader(source)

@app.post("/detibot/insert_faqsource")
async def SourceFaq(source: Faq_Source):
    print(source)
    #inserts the source object into the db
    qstore.delete_vectors(source.question)
    db.insert_source(source)
    #loads the new source object
    qstore.index_faq(source)

#------------------------ endpoints to delete sources in the system------------------------------
@app.delete("/detibot/delete_urlsource/{id}")
async def deleteUrlSource(id: int):
    current_source = db.get("SELECT file_path FROM file_source WHERE id = %s",[id])
    qstore.delete_vectors(current_source[0])
    db.delete_url_source(id)

@app.delete("/detibot/delete_filesource/{id}")
async def deleteFileSource(id: int):
    current_source = db.get("SELECT file_path FROM url_source WHERE id = %s",[id])
    if not os.path.exists(current_source[0]):
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        os.remove(current_source[0])
        qstore.delete_vectors(current_source[0])
        db.delete_file_source(id)
        return {"detail": "File deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {e}")

    #falta dar delete na pasta do uploads

@app.delete("/detibot/delete_faqsource/{id}")
async def deleteFaqSource(id: int):
    current_source = db.get("SELECT question FROM faq_source WHERE id = %s",[id])
    qstore.delete_vectors(current_source[0])
    db.delete_faq_source(id)

#------------------------ endpoints to update sources in the system------------------------------
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
    
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    updated_source = File_Source(file_name=file.filename,file_path=file_location,loader_type=file.content_type,description=descript)
    db.update_file_source(id, updated_source)
    load.file_loader(updated_source)

@app.put("/detibot/update_faqsource/{id}")
async def updateFaqSource(id: int,source: Faq_Source):
    db.update_faq_source(id, source)
    qstore.delete_vectors(source.question)
    qstore.index_faq(source)
