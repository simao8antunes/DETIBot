#This class contains all the functions and calls to the other classes
#To execute the neccessary methods to index the loaded sources  
#Into the vector store trough the 'indexer' method.
from llama_index.core import VectorStoreIndex
from llama_index.core import Settings
from llama_index_client import SentenceSplitter
from Services.storing import Qdrantdb
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

db = Qdrantdb()

class Indexing:

    def __init__(self):
        self.text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=10)
        Settings.text_splitter = self.text_splitter

    def indexer(self,doc):
        index = VectorStoreIndex.from_documents(
            doc, transformations=[self.text_splitter]
        )
        return {"Indexing": "Successfull"}
    
"""  

from llama_index.core import SimpleDirectoryReader

documents = SimpleDirectoryReader("./data").load_data()

url = "http://localhost:6333"

# Load the embedding model
model_name = "BAAI/bge-large-en"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}

embeddings = HuggingFaceEmbedding(
    model_name=model_name,
)

qdrant = QdrantVectorStore.from_documents(
    documents,
    embeddings,
    url=url,
    prefer_grpc=False,
    collection_name="vector_db"
)

print("Vector DB Successfully Created!")"""