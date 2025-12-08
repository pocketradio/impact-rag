import chromadb
import os

def chromaDBstorage(chunks):
    os.makedirs("chroma_db", exist_ok = True)
    
    client = chromadb.PersistentClient(path="chroma_db")
    
    
    # try:
    #     client.delete_collection("code_chunks")
    # except:
    #     print('no collection to delete. Proceeding...')
    
    
    collection = client.create_collection("code_chunks")
    
    
    ids = [] 
    embeddings = []
    metadatas = []
    documents = []
    
    
    # preparation using chunks 
    for chunk in chunks:
        ids.append(chunk["id"])
        embeddings.append(chunk["embedding"])
        metadatas.append({
            "name" : chunk["name"],
            "repo_id" : chunk["repo_id"],
            "file" : chunk["file"],
            "type" : chunk["type"]
        })
        documents.append(chunk["code"])
    
    # vector store : 
    collection.add(
        ids=ids,
        metadatas=metadatas,
        embeddings=embeddings,
        documents=documents
    )
    
    