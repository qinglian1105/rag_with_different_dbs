from initialize.sharing import INIT_JSON, get_variables
import os


def list_files_in_folder(folder_path):
    try: 
        list_files = []   
        items = os.listdir(folder_path)                  
        for item in items:
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):                
                if item[-4:] == ".txt":
                    list_files.append(item)
        return list_files                    
    except Exception as e:
        print(e)
        return []
    

def read_text_file(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            content = file.read()
        return [content]    
    except Exception as e:
        print(e)
        return [] 


def create_data_for_db():
    try:  
        folder_path = get_variables(INIT_JSON)["document_path"]      
        list_files = list_files_in_folder(folder_path)
        simulates = []
        for f in list_files:
            doc = dict()
            title = f.replace(".txt","")
            content = read_text_file(os.path.join(folder_path, f))        
            doc["title"] = title
            doc["content"] = content[0]
            simulates.append(doc)
        return simulates 
    except Exception as e:
            print(e)
            return []       