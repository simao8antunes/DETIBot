#This file contains all the functions and calls to the other classes
#To execute the neccessary methods to store data.  
#In this file we have 2 classes: "Qdrant" and "H2".
#This classes provide the necessary methods to Insert, Delete or modify data in Qdrant and H2.

from Services import File_Source, URL_Source
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition,MatchValue, models
from langchain_community.vectorstores.qdrant import Qdrant
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from datetime import datetime, timedelta
import mysql.connector

QDRANT_URL = "http://localhost:6333" #url="http://qdrantdb:6333" <- docker || local -> url="http://localhost:6333"
MYSQL_HOST = "localhost" #"mysqldb" <-docker || local -> "localhost"

class QStore:  

    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device':'cpu'}, # here we will run the model with CPU only
        encode_kwargs = {
            'normalize_embeddings': True # keep True to compute cosine similarity
        })
    
    def index_documents(self, chunks):
        
        index = Qdrant.from_documents(
            chunks,
            embedding=self.embeddings,
            url=QDRANT_URL,  
            collection_name="db"
        )
        index.client.close()

    def object_retriever(self):
        client = QdrantClient(url=QDRANT_URL)
        self.vector_store = Qdrant(client=client,embeddings=self.embeddings,collection_name="db")
        retriever = self.vector_store.as_retriever()
        return retriever, client
    
    def delete_vectors(self, payload_source="./Data/info.pdf"):
        client = QdrantClient(url=QDRANT_URL)
        if client.collection_exists(collection_name="db"):
            delete_filter=Filter(
                must=[
                    FieldCondition(
                        key="metadata.source",
                        match=MatchValue(value=payload_source),
                        )
                    ]
                )
            
            client.delete(collection_name="db", points_selector=delete_filter)
        client.close()

class MySql:
    
    def __init__(self):
        
        # Connect to MySQL
        try:
            self.conn = mysql.connector.connect(
                host=MYSQL_HOST,
                user="bot",
                password="pi2024",
                database="Detibot"
            )

            if self.conn.is_connected():
                print("Connected to MySQL database")

                # Perform database operations
                self.cursor = self.conn.cursor()

        except mysql.connector.Error as e:
            print("Error connecting to MySQL:", e)

    def insert_source(self,source):# inserts the source object 
        #insert_sql = "INSERT INTO source (url_path,loader_type,descript,update_period_id) VALUES (%s,%s,%s,%s)"
        Id = 0
        if source.update_period == "Daily":
            Id = 1
        elif source.update_period == 'Weekly':
            Id = 2
        elif source.update_period == 'Monthly':
            Id = 3
        elif source.update_period == 'Quarter':
            Id = 4
        
        
        if isinstance(source, File_Source): 
            insert_sql = (
                "INSERT INTO file_source "
                "(file_name,file_path, loader_type, descript) "
                "VALUES (%s, %s, %s, %s)"
            )
            params = (source.file_name,source.file_path, source.loader_type, source.description)
        elif isinstance(source, URL_Source):
            insert_sql = (
                "INSERT INTO url_source "
                "(url_link, paths, descript, wait_time, recursive_url, update_period_id) "
                "VALUES (%s, %s, %s, %s, %s, %s)"
            )
            params = (source.url, ','.join(source.paths), source.description, source.wait_time, source.recursive, Id)
        else:
            return "Invalid source type"

        try:
            self.cursor.execute(insert_sql,params) # maybe put here a logger and a try/ctach
            self.conn.commit()
        except mysql.connector.Error as e:
            print("Error inserting to MySQL:", e)

    def update_source(self,source):# updates the source object 
        pass
    def delete_source(self,source):# deletes the source object  
        pass

    def update_time(self,idx):# updates the period time in the update time table 
        update_sql = """
        UPDATE update_time SET update_period = %s WHERE id = %s
        """
        if idx >= 1 or idx <= 4:
            if idx == 1:
                time = datetime.now().replace(hour=0,minute=0,second=0,microsecond=0) + timedelta(days=1)
            elif idx == 2:
                time = datetime.now().replace(hour=0,minute=0,second=0,microsecond=0) + timedelta(weeks=1)
            elif idx == 3:
                time = datetime.now().replace(hour=0,minute=0,second=0,microsecond=0) + timedelta(weeks=4)
            else:
                time = datetime.now().replace(hour=0,minute=0,second=0,microsecond=0) + timedelta(weeks=12)
            
            self.cursor.execute(update_sql,[str(time.strftime('%Y-%m-%d %H:%M:%S')),idx])# maybe put here a logger and a try/ctach
            self.conn.commit()
            return str(time)
        else:
            return "invalid index"
    def get(self,query,arg):# implements the query, NOTA: maybe it is required more methods of this kind
        self.cursor.execute(query,arg)# maybe put here a logger and a try/ctach
        return self.cursor.fetchall()
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()