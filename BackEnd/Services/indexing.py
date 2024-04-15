#This class contains all the functions and calls to the other classes
#To execute the neccessary methods to index the loaded sources  
#Into the vector store trough the 'indexer' method.

from Services.rag import Rag

rag = Rag()
class Indexing:
        def index(self, documents):
            rag.index_documents(documents)
            return {"Indexing": "Successfull"}
    