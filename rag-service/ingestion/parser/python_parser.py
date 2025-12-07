import ast
from typing import List

def ast_parser(files):

    nodes = []
    edges = []
    current_fn = ""
    current_class = ""
    
    
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            source = f.read()
        
        tree = ast.parse(source)
        
        for element in ast.walk(tree):
            
            if isinstance(element, ast.FunctionDef):
                current_fn = element.name
                if current_class:
                    id = f"{file}:{current_class}.{element.name}" 
                else:
                    id = f"{file}:{element.name}" 
                    current_class = ""
                    
                nodes.append({
                    # "id": f"{file}:{element.name}" ,
                    "id" : id,
                    'type': "function",
                    "name" : element.name, 
                    "lineno" : element.lineno, 
                    "file": file
                    })

                
            elif isinstance(element, ast.ClassDef):
                current_fn = "" # to avoid leaks on entering a class if a fn is called from inside the class
                nodes.append({
                    "type" : "class", 
                    "name" : element.name,
                    "lineno" : element.lineno,
                    "id" : f"{file}:{element.name}",
                    "file" : file
                })
                
                current_class = element.name
                
            elif isinstance(element, ast.ImportFrom): # for type : from x import y
                if (element.module):
                    edges.append({"kind": "imports", "source":file, "target" : element.module })
            
            elif isinstance(element, ast.Import): #  for type : import xyz
                for alias in element.names: #since ast gives imports as alias objs. 
                    edges.append({
                        "kind": "imports", 
                        "source" : file, 
                        "target": alias.name
                        })
                    
                    # element.names -> gives list. alias.name since each alias has a .name prop

            elif isinstance(element, ast.Call):
                
                if isinstance(element.func, ast.Name): # for type : xyz ()
                    
                    if current_class: # in case the function call is being made inside a class. 
                        edges.append({
                            "kind" : "calls",
                            "source" : f"{file}:{current_class}.{current_fn}",
                            "target" : element.func.id
                        })
                    else:
                        edges.append({
                            "kind" : "calls",
                            "source" : f"{file}:{current_fn}",
                            "target" : element.func.id
                        })
                        
                
                else: # its an attribute ; for type : object.xyz() so elem.func.attr will give xyz
                    if current_class:
                        
                        edges.append({
                            "kind" : "calls",
                            "source" : f"{file}:{current_class}.{current_fn}",
                            "target" : element.func.attr
                        })
                    
                    else:
                        
                        edges.append({
                            "kind" : "calls",
                            "source" : f"{file}:{current_fn}",
                            "target" : element.func.attr
                            
                        })
                        
        # reset globals for next file in loop
        current_class = ""
        current_fn = ""
        
    return nodes, edges


def edge_name_resolution(nodes : List, edges: List):
    
    node_lookup = {}
    
    for node in nodes:  
        node_lookup.setdefault(node["name"], []).append(node["id"]) # for list of ids since multiple files may have same fn names

    for e in edges:
        target = e["target"]
        if target in node_lookup: # o(1) lookup 
            e["target"] = node_lookup[target][0]