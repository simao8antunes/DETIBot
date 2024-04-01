#This class contains all the functions and calls to the other classes
#To execute the neccessary methods to load the source provided in the
#'loader' method.
from llama_index.core import SimpleDirectoryReader
from Services.indexing import Indexing

#index = Indexing()

class Loading:

    def loader(self,url, loader_type):
        documents = SimpleDirectoryReader("./Data").load_data()

        print("loaded document: %s",documents)
        
        #index.indexer(documents)
        return {"Loading": "Successfull"}
