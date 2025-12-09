from pipeline.embedding import embedding_pipeline
from pipeline.embedding import embed_query
from pipeline.vectorstore import query_collection

def transform_query(query : str):
    embedded_query = embed_query(query)
    return embedded_query


def retrieve(embedded_query : str,   repo_id : str , top_k : int =1, min_score : float = 0.1 ):
    results = query_collection(embedded_query = embedded_query, top_k= top_k, repo_id= repo_id)
    # print(type(results), "\n\n", type(results[0])) # -> gives a list, dictionary
    return results
    