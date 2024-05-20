#This class contains all the functions and calls to the other classes
#To execute the neccessary methods to index the loaded sources  
#Into the vector store trough the 'indexer' method.
from langchain_text_splitters import RecursiveCharacterTextSplitter
from Services import QStore,Rag

qstore = QStore()
rag = Rag()
class Indexing:

    def __init__(self,size=256,overlap=25):
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=size, chunk_overlap=overlap)

    def index(self, documents):
        chunks = self.text_splitter.split_documents(documents)
        qstore.index_documents(chunks)
        return {"Indexing": "Successfull"}
