from bot import CrawJUD
from app import app

import os
import sys
import json
import pathlib
import platform
import subprocess

def initBot(argv: str):
    
    master = CrawJUD(argv)

def install_cert(data:dict, path_cert):

    comando = ["certutil", "-importpfx", "-user", "-f", "-p", data.get("senha_token"), "-silent", path_cert]
    try:
        # Quando você passa uma lista, você geralmente não deve usar shell=True
        resultado = subprocess.run(comando, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # print("Certificado importado com sucesso.")
        # print("Saída:", resultado.stdout)
        
    except subprocess.CalledProcessError as e:
        print("Erro ao importar o certificado:")
        print(e.stdout)

initBot(sys.argv[1])