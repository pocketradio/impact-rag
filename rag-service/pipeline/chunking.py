from uuid import uuid4
import ast
def make_chunks(nodes, repo_id):
    

    chunks = []
    file_cache = {}
    
    
    for node in nodes:
        
        start = node["line_no"] - 1
        end = node["end_line_no"]
        size = end - start
        
        if node["file"] not in file_cache:
            with open(node["file"], "r",encoding='utf-8') as f:
                file_cache[node["file"]] =  f.read().splitlines()
                
        code = "\n".join(file_cache[node["file"]][start : end])
        
        if node["type"] == 'function':
            # code = "\n".join(file_cache[node["file"]][start : end])
            chunks.append({
                "metadata" : {
                    "type" : "function",
                    "repo_id" : repo_id,      
                    "name" : node["name"],
                    "id" : str(uuid4()),
                    "file" : node["file"],
                },

                "code" : code,
            })
            
        elif node["type"] == 'method':
            # code = "\n".join(file_cache[node["file"]][start : end])
            
            chunks.append({
                "metadata" : {
                    "type" : "method",
                    "repo_id" : repo_id,
                    "name" : node["name"],
                    "id" : str(uuid4()),       
                    "class": node["class"],
                    "file" : node["file"],                
                },
                
                
                "code" : f"\nclass {node['class']}:\n{code}",
            })

        elif node["type"] == "class":

            chunks.append({
                "metadata" :{
                    "type" : "class_summary",
                    "repo_id" : repo_id,
                    "name" : node["name"],
                    "id" : str(uuid4()),  
                    "file" : node["file"],
                },
                
                "code": "",
                "methods" : node["methods"]
            })
            
        
            
            
            
    # all_chunks = []
    # file_cache = {}         # stores code lines from each file 
        
    # for node in nodes:
    
    #     if node["file"] not in file_cache:
    #         with open(node["file"], "r",encoding='utf-8') as f:
    #             file_cache[node["file"]] =  f.read().splitlines()  #filecache key -> filename , value -> array of all code lines
        
    #     file_text = file_cache[node["file"]]

    #     start = node["lineno"]-1
    #     end = node["endlineno"]
    #     size = node["endlineno"] - node["lineno"] + 1
        
    #     lines = file_text[start:end]
        
    #     MAX_LINES = 8
        
    #     if size > MAX_LINES:
                
    #         for i in range(0, size, MAX_LINES):
                
    #             sub_chunk = lines[i:i+MAX_LINES]
                
    #             all_chunks.append({
    #                 "code" : "\n".join(sub_chunk), 
    #                 "file" : node["file"],
    #                 "name" : node["name"],
    #                 "type" : node["type"],
    #                 "id" : str(uuid4()),
    #                 "repo_id" : repo_id
    #             })
    #         continue
        
        
    #     code = "\n".join(lines)
        
    #     all_chunks.append({
    #         "code" : code, 
    #         "file" : node["file"],
    #         "name" : node["name"],
    #         "type" : node["type"],
    #         "id" : str(uuid4()),
    #         "repo_id" : repo_id
    #     })

    # return all_chunks