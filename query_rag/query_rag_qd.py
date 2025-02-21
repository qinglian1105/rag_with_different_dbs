from initialize.sharing import INIT_JSON, get_variables, get_embedding
import requests
import json
import os

      
def points_query(payload): 
    collection_name = get_variables(INIT_JSON)["qd_collection_name"]  
    qdrant_url = get_variables(INIT_JSON)["qdrant_url"]   
    url = f"{qdrant_url}/collections/{collection_name}/points/query"  
    response = requests.post(url, data=json.dumps(payload))
    if response.status_code == 200:
        result = response.json()["result"]["points"]               
        return result
    else:
        print(response)
    
        
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
    payload = {"query": query_embedding,              
                "with_payload": True,
                "limit": 3}
    rows = points_query(payload)
    context = "\n\n".join([f"title: {row['payload']['title']}\ncontent: {row['payload']['content']}" for row in rows])
    added_prompt = "\n(Please provide a brief answer based on the given context.)" 
    prompts = f"Query: {query_str}\nContext:\n{context + added_prompt}"
    return prompts
           

def query_with_qdrant(query_str):
    chat_model = get_variables(INIT_JSON)["pull_models"][0]
    prompts = generate_context(query_str)
    response = generate_response(prompts, chat_model)
    print(f"\n--- Query ---\n\n{query_str}\n")
    print(f"\n--- Response (qdrant) ---\n\n{response}\n\n{"-"*30}")     
