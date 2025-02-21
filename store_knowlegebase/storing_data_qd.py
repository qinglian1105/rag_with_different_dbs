from initialize.sharing import INIT_JSON, get_variables, get_embedding
import requests
import json
import os


def list_all_collections(): 
    qdrant_url = get_variables(INIT_JSON)["qdrant_url"]  
    url = f"{qdrant_url}/collections"
    response = requests.get(url).json()
    if response["status"] == "ok":
        print(response["result"]["collections"])
     

def create_a_collection(collection_name):
    vector_size = get_variables(INIT_JSON)["vector_size"] 
    qdrant_url = get_variables(INIT_JSON)["qdrant_url"] 
    url = f"{qdrant_url}/collections/{collection_name}"
    ds = {"vectors": {"size": vector_size, "distance": "Cosine"}}
    response = requests.put(url, data=json.dumps(ds))
    if response.status_code == 200:
        print(f"Create collection - {collection_name}")        
    else:
        print(response) 


def delete_a_collection(collection_name): 
    qdrant_url = get_variables(INIT_JSON)["qdrant_url"]   
    url = f"{qdrant_url}/collections/{collection_name}"
    response = requests.delete(url)
    if response.status_code == 200:
        print(f"Delete collection - {collection_name}")        
    else:
        print(response)  


def upsert_points(collection_name, points_list): 
    qdrant_url = get_variables(INIT_JSON)["qdrant_url"] 
    url = f"{qdrant_url}/collections/{collection_name}/points"
    ds = {"points": points_list}
    id = ds["points"][0]["id"]
    response = requests.put(url, data=json.dumps(ds))
    if response.status_code == 200:
        print(f"Insert data (id: {id}) to collection '{collection_name}'")        
    else:
        print(response)   


def store_data_to_qdrant(simulate_text): 
    collection_name = get_variables(INIT_JSON)["qd_collection_name"] 
    embedding_model = get_variables(INIT_JSON)["pull_models"][1]  
    create_a_collection(collection_name)
    for idx, example in enumerate(simulate_text):
        dic = {
            "id": idx + 1,
            "payload": {"title": example["title"], "content": example["content"]},
            "vector": get_embedding(example["content"], embedding_model),
        }
        upsert_points(collection_name, [dic])
          
