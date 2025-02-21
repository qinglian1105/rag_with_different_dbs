from initialize.sharing import INIT_JSON, get_variables, get_embedding
import psycopg2
import requests
import json
import os


def connect_db():
    try:
        db_params = get_variables(INIT_JSON)["db_pg_params"]                       
        conn = psycopg2.connect(**db_params)        
        return conn
    except Exception as e:
        print(e)


def generate_response(prompts, chat_model):  
    ollama_url = get_variables(INIT_JSON)["ollama_url"]      
    url = f"{ollama_url}/api/generate"
    model_input = {"model": chat_model, 
                "prompt": prompts, "stream": False}    
    res = requests.post(url, data=json.dumps(model_input), stream=True)            
    if res.status_code == 200:
        reponse = res.json()["response"]  
        return reponse 
    else:
        print(res)


def generate_context(query_str):  
    embedding_model = get_variables(INIT_JSON)["pull_models"][1]  
    query_embedding = get_embedding(query_str, embedding_model)      
    embedding_string = f"[{','.join(map(str, query_embedding))}]"
    table_name = get_variables(INIT_JSON)["ts_table_name"] 

    with connect_db() as conn:
        with conn.cursor() as cur:                          
            cur.execute(f"""
                SELECT title, content, 1 - (embedding <=> %s::vector) AS similarity
                FROM {table_name}
                ORDER BY similarity DESC
                LIMIT 3;
            """, (embedding_string,))    
            rows = cur.fetchall()  

    context = "\n\n".join([f"Title: {row[0]}\nContent: {row[1]}" for row in rows])
    added_prompt = "\n(Please provide a brief answer based on the given context.)" 
    prompts = f"Query: {query_str}\nContext:\n{context+added_prompt}"
    return prompts
          

def query_with_timescale(query_str):
    prompts = generate_context(query_str)
    chat_model = get_variables(INIT_JSON)["pull_models"][0]
    response = generate_response(prompts, chat_model)
    print(f"\n--- Query ---\n\n{query_str}\n")
    print(f"\n--- Response (timescale) ---\n\n{response}\n\n{"-"*30}")
