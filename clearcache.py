import os
import shutil

for root, dirs, files in os.walk(os.path.join(os.getcwd())):
    
    if ".venv" not in root:
        if "__pycache__" in root:
            shutil.rmtree(root)
            
        for file in files:
            if ".exe" in file:
                os.remove(os.path.join(root, file))
