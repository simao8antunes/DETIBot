#This class contains all the functions and calls to the other classes
#To execute the neccessary methods to load the source provided in the
#'loader' method.
#from llama_index.core import SimpleDirectoryReader

from Services.indexing import Indexing
#
#from langchain_text_splitters import RecursiveCharacterTextSplitter
#from langchain_community.document_loaders.pdf import PyPDFLoader

index = Indexing()

class Loading:

    def loader(self,url=None, loader_type=None):
        
        #data = PyPDFLoader("./Data/info.pdf")
#
        #documents = data.load()
#
        #text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
#
        #chunks = text_splitter.split_documents(documents)

        #documents = SimpleDirectoryReader("./Data").load_data()
#
        #print("loaded document: %s",documents)
        #
        index.indexer()
        return {"Loading": "Successfull"}
