import ast
from typing import List

nodes = []
edges = []
# module = {}

def recursive_dfs(current_node, context):
    # context -> { currentfile , currentclass, currentfn }
    
    source = ""
    if context["class"]:
        source = f"{context['file']}:{context['class']}.{context['function']}"
    elif context["function"]:
        source = f"{context['file']}:{context['function']}"
    else:
        source = f"{context['file']}"
    
    
    if isinstance(current_node, ast.ClassDef):
        
        method_names = []

        for child_node in current_node.body:
            if isinstance(child_node,ast.FunctionDef):
                method_names.append(child_node.name)

        nodes.append({
            "type" : "class",
            "line_no" : current_node.lineno,
            "end_line_no" : current_node.end_lineno,
            "file" : context["file"],
            "name" : current_node.name,
            "methods" : method_names
        })
        child_context = {"file" : context["file"], "class" : current_node.name, "function" : context["function"]}

    elif isinstance(current_node, ast.FunctionDef):
        if context["class"]:
            nodes.append({
                "type" : "method",
                "line_no" : current_node.lineno,
                "end_line_no" : current_node.end_lineno,
                "file" : context["file"],
                "name" : current_node.name,
                "class" : context["class"]
            })
        else:
            nodes.append({
                "type" : "function",
                "line_no" : current_node.lineno,
                "end_line_no" : current_node.end_lineno,
                "file" : context["file"],
                "name" : current_node.name,
                "class" : None
            })
            
        child_context = {"file" : context["file"], "class" : context["class"], "function" : current_node.name}
        


    elif isinstance(current_node, ast.ImportFrom ):
        if ( current_node.module ):
            for alias in current_node.names:
                
                edges.append({
                    "type" : "import",
                    "source" : source,
                    "target" : alias.name
                })
        child_context = context
            
        
    elif isinstance(current_node, ast.Import):
        for alias in current_node.names:
            edges.append({
                "type" : "import",
                "source" : source,
                "target" : alias.name
            })
        child_context = context
    
    elif isinstance(current_node, ast.Call):
        if isinstance(current_node.func, ast.Name):
            edges.append({
                "type" : "call",
                "source" : source,
                "target" : current_node.func.id
            })
        elif isinstance(current_node.func, ast.Attribute):
            edges.append({
                "type" : "call",
                "source" : source,
                "target" : current_node.func.attr
            })
        child_context = context
    
    # elif context["class"] == None and context["function"] == None:
    #     module
    
    else:
        child_context = context
        
        
        
        
        
    for child in ast.iter_child_nodes(current_node):
        recursive_dfs(current_node = child, context = child_context)
    
    
    
    
    
    
def ast_parser(files):
    for file in files:
        with open(file, "r", encoding='utf-8') as f:
            source = f.read()

        root_node_of_ast = ast.parse(source)
        recursive_dfs(root_node_of_ast, {"file" : file, "class" : None, "function" : None})
    
    
    return nodes, edges
    
# def ast_parser(files):

#     nodes = []
#     edges = []
#     current_fn = ""
#     current_class = ""
    
    
#     for file in files:
#         with open(file, "r", encoding="utf-8") as f:
#             source = f.read()
        
#         if not file.endswith(".py"):
#             continue
        
#         tree = ast.parse(source)
        
#         for element in ast.walk(tree):
            
#             if isinstance(element, ast.FunctionDef):
#                 current_fn = element.name
#                 if current_class:
#                     id = f"{file}:{current_class}.{element.name}" 
#                 else:
#                     id = f"{file}:{element.name}" 
#                     current_class = ""
                    
#                 nodes.append({
#                     # "id": f"{file}:{element.name}" ,
#                     "id" : id,
#                     'type': "function",
#                     "name" : element.name, 
#                     "lineno" : element.lineno,
#                     "endlineno" : element.end_lineno, 
#                     "file": file
#                     })

                
#             elif isinstance(element, ast.ClassDef):
#                 current_fn = "" # to avoid leaks on entering a class if a fn is called from inside the class
#                 nodes.append({
#                     "type" : "class", 
#                     "name" : element.name,
#                     "lineno" : element.lineno,
#                     "endlineno" : element.end_lineno,
#                     "id" : f"{file}:{element.name}",
#                     "file" : file
#                 })
                
#                 current_class = element.name
                
#             elif isinstance(element, ast.ImportFrom): # for type : from x import y
#                 if (element.module):
#                     edges.append({"kind": "imports", "source":file, "target" : element.module })

#             elif isinstance(element, ast.Import): #  for type : import xyz
#                 for alias in element.names: #since ast gives imports as alias objs. 
#                     edges.append({
#                         "kind": "imports", 
#                         "source" : file, 
#                         "target": alias.name
#                         })
                    
#                     # element.names -> gives list. alias.name since each alias has a .name prop

#             elif isinstance(element, ast.Call):
                
#                 if isinstance(element.func, ast.Name): # for type : xyz ()
                    
#                     if current_class: # in case the function call is being made inside a class. 
#                         edges.append({
#                             "kind" : "calls",
#                             "source" : f"{file}:{current_class}.{current_fn}",
#                             "target" : element.func.id
#                         })
#                     else:
#                         edges.append({
#                             "kind" : "calls",
#                             "source" : f"{file}:{current_fn}",
#                             "target" : element.func.id
#                         })
                        
                
#                 else: # its an attribute ; for type : object.xyz() so elem.func.attr will give xyz
#                     if current_class:
                        
#                         edges.append({
#                             "kind" : "calls",
#                             "source" : f"{file}:{current_class}.{current_fn}",
#                             "target" : element.func.attr
#                         })
                    
#                     else:
                        
#                         edges.append({
#                             "kind" : "calls",
#                             "source" : f"{file}:{current_fn}",
#                             "target" : element.func.attr
                            
#                         })
                        
#         # reset globals for next file in loop
#         current_class = ""
#         current_fn = ""
        
#     return nodes, edges

def edge_name_resolution(nodes : List, edges: List):
    
    node_lookup = {}
    
    for node in nodes:  
        node_lookup.setdefault(node["name"], []).append(node["id"]) # for list of ids since multiple files may have same fn names

    for e in edges:
        target = e["target"]
        if target in node_lookup: # o(1) lookup 
            e["target"] = node_lookup[target][0]
    
    return edges