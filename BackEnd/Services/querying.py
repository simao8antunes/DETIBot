#This class contains all the functions and calls to the other classes
#To execute the neccessary methods to load the source provided in the
#'loader' method.
#from llama_index.core import SimpleDirectoryReader

from Services.indexing import Indexing
from langchain_community.vectorstores.qdrant import Qdrant
from langchain_community.embeddings.huggingface import HuggingFaceInferenceAPIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.pdf import PyPDFLoader
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os
from Services.rag import Rag

rag = Rag()
class Query: 
        def queries(self, question):
            rag.query(question)
            return {"Indexing": "Successfull"}