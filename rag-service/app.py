from fastapi import FastAPI
from pydantic import BaseModel
import os
from ingestion import repo_manager, file_scanner
from ingestion.parser.python_parser import ast_parser, edge_name_resolution


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
    
    return{
        "nodes" : nodes,
        "edges" : edges,
        "repo_id" : req.repo_id,
        "repo_url" : req.repo_url,
        "status" : "Repo cloned and scanned",
        "files" : files
    }