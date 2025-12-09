from uuid import uuid4
def make_chunks(nodes, repo_id):
    
    all_chunks = []
    file_cache = {}         # stores code lines from each file 
        
    for node in nodes:
    
        if node["file"] not in file_cache:
            with open(node["file"], "r",encoding='utf-8') as f:
                file_cache[node["file"]] =  f.read().splitlines()  #filecache key -> filename , value -> array of all code lines
        
        file_text = file_cache[node["file"]]

        start = node["lineno"]-1
        end = node["endlineno"]
        size = node["endlineno"] - node["lineno"] + 1
        
        lines = file_text[start:end]
        
        if size > 30:
                
            for i in range(0, size, 30):
                
                sub_chunk = lines[i:i+30]
                
                all_chunks.append({
                    "code" : "\n".join(sub_chunk), 
                    "file" : node["file"],
                    "name" : node["name"],
                    "type" : node["type"],
                    "id" : str(uuid4()),
                    "repo_id" : repo_id
                })
            continue
        
        
        code = "\n".join(lines)
        
        all_chunks.append({
            "code" : code, 
            "file" : node["file"],
            "name" : node["name"],
            "type" : node["type"],
            "id" : str(uuid4()),
            "repo_id" : repo_id
        })

    return all_chunks