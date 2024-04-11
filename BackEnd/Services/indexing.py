#This class contains all the functions and calls to the other classes
#To execute the neccessary methods to index the loaded sources  
#Into the vector store trough the 'indexer' method.
#from llama_index.core import VectorStoreIndex
#from llama_index.core import Settings
#from llama_index_client import SentenceSplitter
#from Services.storing import Qdrantdb
#from llama_index.vector_stores.qdrant import QdrantVectorStore
#from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from langchain_community.vectorstores.qdrant import Qdrant
from langchain_community.embeddings.huggingface import HuggingFaceInferenceAPIEmbeddings
import os

TOKEN = "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"
os.environ["TOKEN"] = "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"
#db = Qdrantdb()

class Indexing:

    def __init__(self):
        self.embeddings = HuggingFaceInferenceAPIEmbeddings(
            api_key = TOKEN,
            model_name= "BAAI/bge-base-en-v1.5"
        )




    def indexer(self,doc):
        vector_store = Qdrant.from_documents(
            doc,
            self.embeddings,
            url="http://localhost:6333",
            collection_name="db"
        )
        
        return {"Indexing": "Successfull"}
    