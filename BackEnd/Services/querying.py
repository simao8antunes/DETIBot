#This class contains all the functions and calls to the other classes
#To execute the neccessary methods to return an answer to the caller
#Of 'answer_question' method.
#
#from langchain_community.vectorstores.qdrant import Qdrant
#from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
#from langchain_community.embeddings.huggingface import HuggingFaceInferenceAPIEmbeddings
#import os
#
#TOKEN = "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"
#os.environ["TOKEN"] = "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"
#from llama_index.core import VectorStoreIndex
#from Services.storing import Qdrantdb
from qdrant_client import QdrantClient,models
#from llama_index.core import StorageContext
#from llama_index.vector_stores.qdrant import QdrantVectorStore
#from llama_index.embeddings.huggingface import HuggingFaceEmbedding
#from llama_index.llms.huggingface import HuggingFaceInferenceAPI
#from llama_index.core import Settings
#from llama_index.llms.openllm import OpenLLMAPI
class Query: 

    def __init__(self):
        self.client = QdrantClient(host="qdrantdb",port=6333)# (host="qdrantdb",port=6333) <-docker || local -> url="http://localhost:6333"
        if not self.client.collection_exists(collection_name="detibot"):
            self.client.create_collection(
                collection_name="detibot",
                vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
            )
        """if not self.client.collection_exists(collection_name="detibot"):
            self.client.create_collection(collection_name="detibot")
        self.vector_store = QdrantVectorStore(client=self.client, collection_name="detibot")
        self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
        #self.local_llm = OpenLLMAPI(address="http://localhost:3000") #"HuggingFaceH4/zephyr-7b-alpha"
        self.embeded_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
        Settings.embed_model = self.embeded_model
        #Settings.llm = HuggingFaceInferenceAPI(model_name="HuggingFaceH4/zephyr-7b-alpha", token="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")"""

    def answer_question(self,prompt:str):

        #index = VectorStoreIndex.from_vector_store(
        #    vector_store=self.vector_store,
        #)
#
        #query_engine = index.as_query_engine()

        return {"resposta":prompt}

#
        #if search:
        #    most_similar_chunk = search[0]  # Assuming search results are sorted by similarity
        #    similar_text = most_similar_chunk.page_content
        #    
        #    # Initialize tokenizer and model
        #    tokenizer = AutoTokenizer.from_pretrained("t5-base")
        #    model = AutoModelForSeq2SeqLM.from_pretrained("t5-base")
        #    
        #    # Tokenize the similar text
        #    inputs = tokenizer.encode("summarize: " + similar_text, return_tensors="pt", max_length=512, truncation=True)
        #    
        #    # Generate response using the model
        #    outputs = model.generate(inputs, max_length=100, num_beams=4, early_stopping=True)
        #    
        #    # Decode the generated response
        #    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        #    return {"Question":  prompt, "Answer" : generated_text}
        #else:
        #    print("No relevant information found for your query.")
#
        #    self.vector_store.close_connection()