import platform
import subprocess
import requests
import re

import os
import tqdm
import zipfile
import shutil


system = platform.system()

if system == 'Windows':
    
    # Verifica a versão do Chrome instalado
    result = subprocess.check_output(["reg", "query", "HKLM\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Google Chrome", "/v", "DisplayVersion"], text=True)
    match = re.search(r'\d+(\.\d+){2}', result)
    if match:
        code_ver = match.group()
    
    ## Verifica no endpoint qual a versão disponivel do WebDriver 
    results = requests.get(url=f"https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_{code_ver}")
    chrome_version = results.text
    
    ## Baixa o WebDriver conforme disponivel no repositório
    url = f"https://storage.googleapis.com/chrome-for-testing-public/{chrome_version}/win64/chromedriver-win64.zip"
    
elif system == 'Linux':
    
    # Verifica a versão do Chrome instalado
    result = subprocess.check_output(["google-chrome", "--version"], text=True)
    match = re.search(r'\d+(\.\d+){2}', result)
    if match:
        code_ver = match.group()
    
    ## Verifica no endpoint qual a versão disponivel do WebDriver 
    results = requests.get(url=f"https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_{code_ver}")
    chrome_version = results.text
    
    ## Baixa o WebDriver conforme disponivel no repositório 
    url = f"https://storage.googleapis.com/chrome-for-testing-public/{chrome_version}/linux64/chromedriver-linux64.zip"
    
    
# Certifique-se de que a pasta de destino exista
os.makedirs('webdriver', exist_ok=True)



"""
Faça a solicitação para obter o conteúdo do arquivo
"""
v_chrome_version = chrome_version.replace(".","_")

filename = ''

if platform.system() == "Windows":
    filename = f"chromedriver{v_chrome_version}.exe"
else:
    filename = f"chromedriver{v_chrome_version}"
    
chromdriver_path = os.path.join(os.getcwd(), 'webdriver', filename)

if not os.path.exists(chromdriver_path):
    response = requests.get(url, stream=True)

    # Obtenha o tamanho total do arquivo, se disponível
    total_size = int(response.headers.get('content-length', 0))

    # Crie uma barra de progresso usando tqdm
    with tqdm(total=total_size, unit='B', unit_scale=True, desc='Baixando Webdriver', leave=True) as pbar:
        with open(os.path.join('webdriver', os.path.basename(url)), 'wb') as file:
            for data in response.iter_content(chunk_size=1024):
                # Atualize a barra de progresso
                pbar.update(len(data))
                
                # Escreva os dados no arquivo
                file.write(data)

    file_name = os.path.join('webdriver', os.path.basename(url))
            
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        

        for member in zip_ref.namelist():
            # Construa o caminho de destino removendo o nome do arquivo
            destino = os.path.join('webdriver', os.path.basename(member))

            # Extraia o membro individualmente
            with zip_ref.open(member) as source, open(destino, 'wb') as target:
                target.write(source.read())


    if system == "Linux":
        
        for item in ["chromedriver-linux64.zip", "LICENSE.chromedriver"]:
            os.remove(f"{os.path.join(os.getcwd())}/webdriver/{item}")
        
        subprocess.run(["chmod", "775", f"{os.path.join(os.getcwd(), 'webdriver', 'chromedriver')}"])
        
        replace = os.path.join(os.getcwd(), 'webdriver', f"chromedriver{v_chrome_version}")
        old = os.path.join(os.getcwd(), 'webdriver', 'chromedriver')
        rename_chromedriver = shutil.move(old, replace)
        p = os.path.join('webdriver', f"chromedriver{v_chrome_version}")
    
    elif system == "Windows":
        
        replace = os.path.join(os.getcwd(), 'webdriver', f"chromedriver{v_chrome_version}.exe")
        old = os.path.join(os.getcwd(), 'webdriver', 'chromedriver.exe')
        rename_chromedriver = shutil.move(old, replace)
        p = os.path.join('webdriver', f"chromedriver{v_chrome_version}.exe")
        

elif os.path.exists(chromdriver_path): 
    
    p = chromdriver_path