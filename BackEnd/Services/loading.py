#This class contains all the functions and calls to the other classes
#To execute the neccessary methods to load the source provided in the
#'loader' method.
#from llama_index.core import SimpleDirectoryReader

from Services import URL_Source, File_Source,Indexing,QStore

from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders import Docx2txtLoader, CSVLoader, JSONLoader, UnstructuredHTMLLoader, TextLoader

import os
from Services import urlLoader,Rag

qstore = QStore()
indexer = Indexing()
PDF_PATH = "./Data"
rag = Rag()

class Loading:

    def url_loader(self, source: URL_Source):
        qstore.delete_vectors(source.url)
        documents=self.load_urls(source)
        indexer.index(documents)
        return {"Loading": "Successfull"}
    
    def file_loader(self, source: File_Source):
        qstore.delete_vectors(source.file_path)
        if source.loader_type == "pdf":
            documents = self.load_pdf()
        elif source.loader_type == "csv":
            documents = self.load_csv()
        elif source.loader_type == "docx":
            documents = self.load_docx()
        elif source.loader_type == "json":
            documents = self.load_csv()
        elif source.loader_type == "html":
            documents = self.load_json()
        else:
            documents = self.load_text()
        indexer.index(documents)
        return {"Loading": "Successfull"}
    
    def load_csv(self, source):
        loader = CSVLoader(file_path=source.url)
        return loader.load()
    
    def load_docx(self, source):
        #%pip install --upgrade --quiet  docx2txt
        loader = Docx2txtLoader(file_path=source.url)
        return loader.load()
    
    def load_json(self, source):
        loader = JSONLoader(file_path=source.url)##ver documentaçao para ver se é assim
        return loader.load()
    
    def load_html(self, source):
        loader = UnstructuredHTMLLoader(file_path=source.url)
        return loader.load()
    
    def load_text(self, source):
        loader = TextLoader(file_path=source.url)
        return loader.load()
    
    def load_pdf(self, source):
        loader = PyPDFLoader(file_path=source.url)
        return loader.load()
    
    def load_urls(self, source:URL_Source):
        loader = urlLoader(urls=[source.url], browser="chrome", headless=True)
        return loader.load(wait_time=source.wait_time, recursive=source.recursive, paths=source.paths)

    



