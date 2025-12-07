import os
def scan(repo_path):
    
    files = []
    
    for root, dirs, filenames in os.walk(repo_path):
        for f in filenames:
            if f.endswith((".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".css")):
                files.append(os.path.join(root, f))
    
    return files