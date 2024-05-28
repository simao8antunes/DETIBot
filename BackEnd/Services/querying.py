#This class contains all the functions and calls to the other classes
#To execute the neccessary methods to load the source provided in the
#'loader' method.
#from llama_index.core import SimpleDirectoryReader

from langchain_community.llms.ollama import Ollama
from langchain_core.prompts import PromptTemplate
from langchain.chains.retrieval_qa.base import RetrievalQA
import textwrap
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain


from Services.storing import QStore
qstore = QStore()

class Query: 

    def __init__(self):
        self.llm = Ollama(model="llama3", temperature=0) # ,base_url="http://ollama:11434" <- docker || local -> sem o ,base_url="http://ollama:11434"
        
    def format_history(self, chat_history):
        history = ""
        count = 0
        for message in chat_history:
            history += f"message_id: {count}, message: {message}"
            count += 1
        return history

    def queries(self, question, language,chat):
        retriever, client = qstore.object_retriever()
        history = self.format_history(chat)
        if language == "en":
            template = """
                ### System:
                Always answer in english.
                The following information is your only source of truth, only answer the question with the provided context, if you are unable to answer from that, tell the user “I’m having trouble finding an answer for you"
                You are an respectful and honest assistant. You have to answer the user's questions using only the context \
                provided to you. If you don't know the answer, just say you don't know. Don't try to make up an answer.
                Only use infromation from history if the user input ask you to.
                ### History:
                {history}
                ### Context:
                {context}
                ### User:
                {input}
                ### Response:
                """
        elif language == "pt":
            template = """

                ### System:
                Always answer in portuguese.
                The following information is your only source of truth, only answer the question with the provided context, if you are unable to answer from that, tell the user “I’m having trouble finding an answer for you"
                You are an respectful and honest assistant. You have to answer the user's questions using only the context \
                provided to you. If you don't know the answer, just say you don't know. Don't try to make up an answer.
                Only use infromation from history if the user input ask you to.
                ### History:
                {history}
                ### Context:
                {context}
                ### User:
                {input}
                ### Response:
                """


        # Creating the prompt from the template which we created before
        prompt = PromptTemplate.from_template(template)
        qa_chain = create_stuff_documents_chain(self.llm, prompt)
        chain = create_retrieval_chain(retriever, qa_chain)
        input_data = {
            'input': question,
            'history': history  # add history to input data
        }
        text = chain.invoke(input_data)
        print(text)
        client.close()
        response = textwrap.fill(text['answer'])
        return {"query": response}