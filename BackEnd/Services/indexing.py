#This class contains all the functions and calls to the other classes
#To execute the neccessary methods to index the loaded sources  
#Into the vector store trough the 'indexer' method.

from llama_index.core import VectorStoreIndex
#from Services.storing import Qdrantdb
import qdrant_client
from llama_index.core import StorageContext
from llama_index.core import Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

#db = Qdrantdb()

class Indexing:

    def __init__(self):
        self.client = qdrant_client.QdrantClient(host="127.0.0.1",port=6333)
        self.vector_store = QdrantVectorStore(client=self.client, collection_name="paul_graham")
        self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
        #self.local_llm = OpenLLM("HuggingFaceH4/zephyr-7b-alpha")
        self.embeded_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
        Settings.embed_model = self.embeded_model
        


    def indexer(self,doc):
        #embendings = self.embeded_model.get_text_embedding(doc)
        index = VectorStoreIndex.from_documents(
            show_progress=True,
            documents=doc,
            storage_context=self.storage_context   
        )
#
        #VectorStoreIndex.insert_nodes
        #print(embendings)
        self.client.close()
        return {"Indexing": "Successfull"}
    