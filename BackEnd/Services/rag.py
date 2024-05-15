# rag.py
from langchain_community.vectorstores.qdrant import Qdrant
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.pdf import PyPDFLoader
from qdrant_client import QdrantClient
from langchain_community.llms.ollama import Ollama
from langchain_core.prompts import PromptTemplate
from langchain.chains.retrieval_qa.base import RetrievalQA
import textwrap


from Services.seleniumLoader import SeleniumURLLoaderWithWait
from Services import URL_Source

class Rag:
    def __init__(self, path=None):
        self.token = "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"
        self.llm = Ollama(model="llama2", temperature=0) # ,base_url="http://ollama:11434" <- docker || local -> sem o ,base_url="http://ollama:11434"
        self.path = path
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=256, chunk_overlap=25)
        self.embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device':'cpu'}, # here we will run the model with CPU only
        encode_kwargs = {
            'normalize_embeddings': True # keep True to compute cosine similarity
        }
    )


    def load_documents(self):
        data = PyPDFLoader("./Data/info.pdf")
        return data.load()
    

    def load_urls(self, source:URL_Source):
        loader = SeleniumURLLoaderWithWait(urls=[source.url], browser="chrome", headless=True)
        return loader.load(wait_time=source.wait_time, recursive=source.recursive, paths=source.paths)

    def index_documents(self, documents):
        
        chunks = self.text_splitter.split_documents(documents)
        index = Qdrant.from_documents(
            chunks,
            embedding=self.embeddings,
            url="http://localhost:6333", #url="http://qdrantdb:6333" <- docker || local -> url="http://localhost:6333"
            collection_name="db"
        )
        index.client.close()

    def query(self, question):
        client = QdrantClient(url="http://localhost:6333") #url="http://qdrantdb:6333" <- docker || local -> url="http://localhost:6333"
        self.vector_store = Qdrant(client=client,embeddings=self.embeddings,collection_name="db")
        retriever = self.vector_store.as_retriever()

        template = """
        ### System:
        You are an respectful and honest assistant. You have to answer the user's questions using only the context \
        provided to you. If you don't know the answer, just say you don't know. Don't try to make up an answer.

        ### Context:
        {context}

        ### User:
        {question}

        ### Response:
        """

        # Creating the prompt from the template which we created before
        prompt = PromptTemplate.from_template(template)

        chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=retriever, # here we are using the vectorstore as a retriever
            chain_type="stuff",
            return_source_documents=True, # including source documents in output
            chain_type_kwargs={'prompt': prompt} # customizing the prompt
        )

        response = chain({'query': question})
        client.close()

        # Wrapping the text for better output in Jupyter Notebook
        wrapped_text = textwrap.fill(response['result'], width=100)
        print(wrapped_text)
        return wrapped_text

