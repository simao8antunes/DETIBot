# rag.py

from langchain_community.vectorstores.qdrant import Qdrant
from langchain_community.embeddings.huggingface import HuggingFaceInferenceAPIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.pdf import PyPDFLoader
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from qdrant_client import QdrantClient, models

class Rag:
    def __init__(self, path=None):
        self.token = "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"
        self.path = path
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=256, chunk_overlap=25)
        self.embeddings = HuggingFaceInferenceAPIEmbeddings(
            api_key=self.token,
            model_name="BAAI/bge-base-en-v1.5"
        )


    def load_documents(self):
        data = PyPDFLoader(self.path)
        return data.load()

    def index_documents(self, documents):
        
        chunks = self.text_splitter.split_documents(documents)
        index = Qdrant.from_documents(
            chunks,
            embedding=self.embeddings,
            url="http://qdrantdb:6333", #url="http://qdrantdb:6333" <- docker || local -> url="http://localhost:6333"
            collection_name="db"
        )
        index.client.close()


        index.client.close()

    def query(self, question):
        client = QdrantClient(url="http://qdrantdb:6333") #url="http://qdrantdb:6333" <- docker || local -> url="http://localhost:6333"
        self.vector_store = Qdrant(client=client,embeddings=self.embeddings,collection_name="db")
        search = self.vector_store.similarity_search(question)
        client.close()
        if search:
            most_similar_chunk = search[0]
            similar_text = most_similar_chunk.page_content

            from transformers import pipeline
            generator = pipeline('text-generation', model='NOVA-vision-language/GlorIA-1.3B')
            resposta = generator(similar_text, do_sample=True, min_length=50)
            
            tokenizer = AutoTokenizer.from_pretrained("t5-base")
            model = AutoModelForSeq2SeqLM.from_pretrained("t5-base")
            
            inputs = tokenizer.encode(similar_text, return_tensors="pt", max_length=512, truncation=True)
            
            outputs = model.generate(inputs, max_length=100, num_beams=4, early_stopping=True)
            
            generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

            return generated_text
        else:
            return "No relevant information found for your query."
