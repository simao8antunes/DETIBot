#This class contains all the functions and calls to the other classes
#To execute the neccessary methods to index the loaded sources  
#Into the vector store trough the 'indexer' method.

from llama_index.core import VectorStoreIndex
#from Services.storing import Qdrantdb
from qdrant_client import QdrantClient, models 
from llama_index.core import StorageContext
from llama_index.core import Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


class Indexing:

    def __init__(self):
        self.client = QdrantClient(url="http://localhost:6333") # (host="qdrantdb",port=6333) <-docker || local -> url="http://localhost:6333"
        if not self.client.collection_exists(collection_name="detibot"):
            self.client.create_collection(
                collection_name="detibot",
                vectors_config=models.VectorParams(size=100, distance=models.Distance.COSINE),
            )
        self.vector_store = QdrantVectorStore(client=self.client, collection_name="detibot")
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
    