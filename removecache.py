import os
import shutil

for root, dirs, files in os.walk(os.path.join(os.getcwd())):

    if "__pycache__" in root:
        shutil.rmtree(root)
