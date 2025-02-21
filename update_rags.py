import read_documents.read_docs as rds
import store_knowlegebase.storing_data_ts as kts
import store_knowlegebase.storing_data_qd as kqd


def setting_knowledgebase_timescale(simulate_text):    
    kts.drop_tb()
    kts.create_tb()
    kts.insert_documents(simulate_text)
    kts.select_documents()


def setting_knowledgebase_qdrant(simulate_text):
    kqd.delete_a_collection("qd_collection")
    kqd.store_data_to_qdrant(simulate_text)    


def main():   
    # Read documents       
    simulate_text = rds.create_data_for_db()
       
    # Update knowledgebases
    setting_knowledgebase_timescale(simulate_text)
    setting_knowledgebase_qdrant(simulate_text)

    
if __name__ == "__main__":
    main()