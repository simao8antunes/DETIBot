#This class contains all the functions and calls to the other classes
#To execute the neccessary methods to load the source provided in the
#'loader' method.
#from llama_index.core import SimpleDirectoryReader

from langchain_community.llms.ollama import Ollama
from langchain_core.prompts import PromptTemplate
from langchain.chains.retrieval_qa.base import RetrievalQA
import textwrap

from Services import QStore,Rag

qstore = QStore()
rag = Rag()
class Query: 

    def __init__(self):
        self.llm = Ollama(model="llama2", temperature=0) # ,base_url="http://ollama:11434" <- docker || local -> sem o ,base_url="http://ollama:11434"

    def queries(self, question):
        retriever, client = qstore.object_retriever()
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
        text = chain({'query': question})
        client.close()
        # Wrapping the text for better output in Jupyter Notebook
        response = textwrap.fill(text['result'], width=100)
        print(response)
        return {"query": response}