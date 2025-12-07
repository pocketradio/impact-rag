import os
import shutil
import stat
from git import Repo

def remove_readonly_perms(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path) #retrying the delete again after changing permissions with chmod
    

def delete_if_exists(repo_path):
    try:
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path, onexc = remove_readonly_perms)
            # sends a callback. 
    
    except Exception as e:
        raise Exception(f"Failed to delete existing folder : {str(e)}")
    
    os.makedirs(repo_path, exist_ok=True) # existok actually not needed here but for crash safety


def clone_repo(repo_url, repo_path):
    Repo.clone_from(repo_url, repo_path)