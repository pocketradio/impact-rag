from sentence_transformers import SentenceTransformer
from typing import List
model = SentenceTransformer("intfloat/e5-base-v2")

def embedding_pipeline(chunks : List):

    for chunk in chunks:
        chunk["embedding"] = model.encode(chunk["code"]).tolist() # since encode returns numpY array ( not json serializable)

    print(type(chunks))
    # print(type(chunks[0]),"\n\n\n" ,chunks[0]) 
    return chunks
    # each CHUNK is a dictionary with code, type, name, embeddings, etc. 
    # chunks is a list. 

def embed_query(query : str):
    embedded_query = model.encode(query).tolist()
    return embedded_query