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

indexer = Indexing()
PDF_PATH = "./Data"

class Loading:
    def loader(self):
        # List all PDF files in the "Data" folder
        pdf_files = [f for f in os.listdir(PDF_PATH) if f.endswith('.pdf')]

        for pdf_file in pdf_files:
            pdf_path = os.path.join(PDF_PATH, pdf_file)
            rag = Rag(pdf_path)
            documents = rag.load_documents()
            print(f"Loaded {len(documents)} documents from {pdf_file}")
            indexer.index(documents)

        return {"Loading": "Successful"}