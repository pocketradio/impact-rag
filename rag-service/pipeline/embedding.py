from sentence_transformers import SentenceTransformer
from typing import List
model = SentenceTransformer("intfloat/e5-base-v2")

def embedding_pipeline(chunks : List):

    for chunk in chunks:
        chunk["embedding"] = model.encode(chunk["code"]).tolist() # since encode returns numpY array ( not json serializable)
    
    return chunks
