from fastapi import FastAPI
from pydantic import BaseModel
import os
from ingestion import repo_manager, file_scanner
from ingestion.parser.python_parser import ast_parser, edge_name_resolution
from pipeline.chunking import make_chunks
from pipeline.embedding import embedding_pipeline
from pipeline.vectorstore import chromaDBstorage
from pipeline.retriever import transform_query, retrieve
from llm import generate_llm_response

app = FastAPI()
BASE_DIR = "repos"

class IngestReq(BaseModel):
    repo_id : str
    repo_url : str

@app.post("/ingest")
async def ingest_repo(req : IngestReq):
    
    repo_path = os.path.join(BASE_DIR, req.repo_id) 
    
    repo_manager.delete_if_exists(repo_path=repo_path)
    repo_manager.clone_repo(repo_url = req.repo_url, repo_path = repo_path)
    files = file_scanner.scan(repo_path=repo_path)
    nodes , edges = ast_parser(files)
    edges  = edge_name_resolution(nodes,edges)
    chunks = make_chunks(nodes, req.repo_id)
    embedded_chunks = embedding_pipeline(chunks)
    chromaDBstorage(chunks=embedded_chunks)
    
    
    # for postman testing
    
    # return{
    #     "nodes" : nodes,
    #     "edges" : edges,
    #     "repo_id" : req.repo_id,
    #     "repo_url" : req.repo_url,
    #     "files" : files,
    #     "embedded_chunks" : embedded_chunks,
    # }
    
    return {
		"repo_id": req.repo_id,
		"status": "ingestion complete"
	}
    

class QueryRequest(BaseModel):
    user_query : str
    repo_id : str
    repo_url : str

@app.post("/query")

async def query_user_input(req : QueryRequest):
    embedded_query = transform_query(query = req.user_query)
    retrieved_results = retrieve(embedded_query, repo_id=req.repo_id)
    llm_response = generate_llm_response(retrieved_results, user_query=req.user_query)
    
    return llm_response