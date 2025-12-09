import chromadb
import os

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection("code_chunks")

def chromaDBstorage(chunks):
    os.makedirs("chroma_db", exist_ok = True)
    
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
    # print(type(collection[0], 'is the collection 0 type'))
    

def query_collection(embedded_query, top_k, repo_id):
    results = collection.query(
        query_embeddings = [embedded_query],
        where = {
            "repo_id" : repo_id
        },
        n_results = top_k
    )
    
    # print("\n\n\n\n ", type(results[0]), 'is the type of results ')
    
    return [
		{
			"id": id,
			"document": doc,
			"metadata": meta,
		}
		for id, doc, meta in zip(
			results["ids"][0],
			results["documents"][0],
			results["metadatas"][0],
		)
	]