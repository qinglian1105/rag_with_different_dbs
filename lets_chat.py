import query_rag.query_rag_ts as qts
import query_rag.query_rag_qd as qqd


def main():       
    # Input prompt to the following variable    
    query_str = "What is NVIDIA’s most popular graphics card for 2024?"  
    # query_str = "What is NVIDIA’s EPS for 2024?"  

    # Responses from different DBs
    qts.query_with_timescale(query_str)    
    qqd.query_with_qdrant(query_str)


if __name__ == "__main__":
    main()