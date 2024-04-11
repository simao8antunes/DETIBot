#This class contains all the functions and calls to the other classes
#To execute the neccessary methods to return an answer to the caller
#Of 'answer_question' method.

from langchain_community.vectorstores.qdrant import Qdrant
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from langchain_community.embeddings.huggingface import HuggingFaceInferenceAPIEmbeddings
import os

TOKEN = "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"
os.environ["TOKEN"] = "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"
class Query: 

    def __init__(self):

        self.embeddings = HuggingFaceInferenceAPIEmbeddings(
            api_key = TOKEN,
            model_name= "BAAI/bge-base-en-v1.5"
        )

        self.vector_store = Qdrant.from_documents(
            url="http://localhost:6333",
            collection_name="db"
        )
              
    def answer_question(self,arg,prompt:str):
        
        search = self.vector_store.similarity_search(prompt)

        if search:
            most_similar_chunk = search[0]  # Assuming search results are sorted by similarity
            similar_text = most_similar_chunk.page_content
            
            # Initialize tokenizer and model
            tokenizer = AutoTokenizer.from_pretrained("t5-base")
            model = AutoModelForSeq2SeqLM.from_pretrained("t5-base")
            
            # Tokenize the similar text
            inputs = tokenizer.encode("summarize: " + similar_text, return_tensors="pt", max_length=512, truncation=True)
            
            # Generate response using the model
            outputs = model.generate(inputs, max_length=100, num_beams=4, early_stopping=True)
            
            # Decode the generated response
            generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            return {"Question":  prompt, "Answer" : generated_text}
        else:
            print("No relevant information found for your query.")

            self.vector_store.close_connection()