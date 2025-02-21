from initialize.sharing import INIT_JSON, get_variables, get_embedding
from psycopg2.extras import execute_values
import psycopg2
import requests
import json
import time
import os


def connect_db():
    try:
        db_params = get_variables(INIT_JSON)["db_pg_params"]                       
        conn = psycopg2.connect(**db_params)        
        return conn
    except Exception as e:
        print(e)


def drop_tb():           
    try:
        table_name = get_variables(INIT_JSON)["ts_table_name"]               
        conn = connect_db()
        cur = conn.cursor()        
        sql_str = f"DROP TABLE {table_name};"
        cur.execute(sql_str)
        conn.commit()
        print(f"---> {sql_str}")
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()


def create_tb():
    try:   
        table_name = get_variables(INIT_JSON)["ts_table_name"]  
        vector_size = get_variables(INIT_JSON)["vector_size"]         
        conn = connect_db() 
        cur = conn.cursor()
        cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ( \
                      id SERIAL PRIMARY KEY, \
                      title TEXT, \
                      content TEXT, \
                      embedding VECTOR({vector_size}));"
                   )                                                                            
        conn.commit()
    except Exception as e:
        print(e)
    finally:    
        cur.close()
        conn.close()        
        print(f"Create table - {table_name})")
      

def insert_documents(documents):      
    time.sleep(3)    
    try:
        table_name = get_variables(INIT_JSON)["ts_table_name"]
        embedding_model = get_variables(INIT_JSON)["pull_models"][1]        
        conn = connect_db()
        cur = conn.cursor() 
        data = [(doc["title"], doc["content"], get_embedding(doc["content"], embedding_model)) for doc in documents]
        sql_str = f"""INSERT INTO {table_name} (title, content, embedding) VALUES %s;"""     
        execute_values(cur, sql_str, data,)
        conn.commit()
    except Exception as e:
        print(f"An error occurred (insert): {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()


def select_documents():        
    try: 
        table_name = get_variables(INIT_JSON)["ts_table_name"]       
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table_name};")
        rows = cur.fetchall()
        for row in rows:
            print(row[0], row[1])
            print(row[2])
            print("-" * 30)
    except Exception as e:
        print(f"An error occurred (select): {e}")        
    finally:
        cur.close()
        conn.close()
