from langchain.document_loaders import PyPDFLoader, DirectoryLoader, PDFMinerLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
import os
from constants import CHROMA_SETTINGS

persist_directory = "db"

def main():
    for root, dirs, files in os.walk("docs"):
        for file in files:
            file_path = os.path.join(root, file)
            print("Processing file:", file_path)  # Add this line for debugging
            if file.endswith(".pdf"):
                print(file)
                loader = PyPDFLoader(file_path)
            if file.endswith(".txt"):
                print(file)
                loader = TextLoader(file_path, encoding='utf-8')
            try:
                documents = loader.load()
            except Exception as e:
                print(f"Error loading file: {file_path}")
                print(e)

    print("splitting into chunks")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)
    #create embeddings here
    print("Loading sentence transformers model")
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    #create vector store here
    print(f"Creating embeddings. May take some minutes...")
    db = Chroma.from_documents(texts, embeddings, persist_directory=persist_directory, client_settings=CHROMA_SETTINGS)
    db.persist()
    db=None 

    print(f"Ingestion complete! You can now run privateGPT.py to query your documents")

if __name__ == "__main__":
    main()