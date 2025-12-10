from dotenv import load_dotenv
load_dotenv()

import os
import cohere
from typing import List

co = cohere.Client(os.getenv("COHERE_API_KEY"))

def rerank_results(query : str, top_k_results : List, top_n : int = 3):
    docs = []
    for item in top_k_results: # results : [{id:[], document:[], metadata:[]}, {....}]
        docs.append(item["document"])
    
    reranked_results = co.rerank(
        query = query,
        documents= docs,
        top_n=top_n
    ).results
    
    final_results = []
    
    for r in reranked_results: # re_res => length = 3
        final_results.append(top_k_results[r.index])
    
    return final_results