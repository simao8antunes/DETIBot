#This file contains all the functions and calls to the other classes
#To execute the neccessary methods to store data.  
#In this file we have 2 classes: "Qdrant" and "H2".
#This classes provide the necessary methods to Insert, Delete or modify data in Qdrant and H2.
from Services import File_Source, URL_Source
from datetime import datetime, timedelta
import mysql.connector

class MySql:
    
    def __init__(self):
        
        # Connect to MySQL
        try:
            self.conn = mysql.connector.connect(
                host="localhost", #host="mysqldb" <-docker || local -> host="localhost"
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
                "(url_path, loader_type, descript, update_period_id) "
                "VALUES (%s, %s, %s, %s)"
            )
            params = (source.url, source.loader_type, source.description, Id)
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
    
# URL_SOURCE
    def list_url_sources(self):
        q = "SELECT * FROM url_source"
        try:
            self.cursor.execute(q)
            urlsource = self.cursor.fetchall()
            formatted_sources = [
                {
                    "id": item[0],
                    "url": item[1],
                    "paths": item[2].split(','), 
                    "update_period": item[6],
                    "description": item[3],  
                    "wait_time": item[4],
                    "recursive": bool(item[5])
                }
                for item in urlsource
            ]
            return formatted_sources
        except mysql.connector.Error as e:
            print(f"Error executing query: {e}")
            return []

        
    def delete_url_source(self, id):
        q = "DELETE FROM url_source WHERE id = %s"
        try:
            self.cursor.execute(q, (id,))
            self.conn.commit()
        except mysql.connector.Error as e:
            print(f"Error executing query: {e}")

    def update_url_source(self, id, source):
        q = """
        UPDATE url_source 
        SET url_link = %s, paths = %s, descript = %s, wait_time = %s, recursive_url = %s, update_period_id = %s 
        WHERE id = %s
        """
        update_period_id = 0
        if source.update_period == "Daily":
            update_period_id = 1
        elif source.update_period == 'Weekly':
            update_period_id = 2
        elif source.update_period == 'Monthly':
            update_period_id = 3
        elif source.update_period == 'Quarter':
            update_period_id = 4
        
        try:
            self.cursor.execute(q, (source.url, ','.join(source.paths), source.description, source.wait_time, source.recursive, update_period_id, id))
            self.conn.commit()
            if self.cursor.rowcount == 0:
                return {"error": "ID not found"}
            return {"message": "Source updated successfully"}
        except mysql.connector.Error as e:
            print(f"Error executing query: {e}")
            return {"error": f"Error executing query: {e}"}

# FILE_SOURCE
    def list_file_sources(self):
        q = "SELECT * FROM file_source"
        try:
            self.cursor.execute(q)
            filesource = self.cursor.fetchall()
            return filesource
        except mysql.connector.Error as e:
            print(f"Error executing query: {e}")
            return []
        
    def delete_file_source(self, id):
        q = "DELETE FROM file_source WHERE id = %s"
        try:
            self.cursor.execute(q, (id,))
            self.conn.commit()
        except mysql.connector.Error as e:
            print(f"Error executing query: {e}")
    

    
    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

