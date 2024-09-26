import os
import shutil
import pathlib
from shutil import SameFileError
from contextlib import suppress
from Scripts.bot.jobs.read_pdf import get_barcode

def copy(parametro: str, path: str, wscodbars: str, pid: str) -> list:
    
    files_list = []
    comprovante_files = []
    guias_files = []
    other_files = []
    all_files = []
    
    for root, dirs, files in os.walk(path):
        
        for file in files:
            
            if parametro in file:
                
                os.makedirs(os.path.join(path, parametro), exist_ok=True)
                parametro_path = os.path.join(path, parametro)
                
                if "comprovante" in file.lower():
                    comprovante_files.append(os.path.join(parametro_path, f"{pid} - {file}"))
                    
                elif "deposito" in file.lower() or "pagamento" in file.lower():
                    guias_files.append(os.path.join(parametro_path, f"{pid} - {file}"))
                       
                else:
                    other_files.append(os.path.join(parametro_path, f"{pid} - {file}"))
                
                with suppress(SameFileError):
                    if "NOMEDAGUIA" in file.upper():
                        guias_files.append(os.path.join(parametro_path, f"{pid} - {file}".replace("NOMEDAGUIA", "GUIA PAGAMENTO")))
                    
                    shutil.copy(os.path.join(root, file), os.path.join(parametro_path, f"{pid} - {file}".replace("NOMEDAGUIA", "GUIA PAGAMENTO")))
    
    files_list = comprovante_files + guias_files
    if len(files_list) > 1:       
        
            
        all_files = files_list + other_files
        check_barcode = get_barcode(files_list[0], files_list[1], wscodbars, parametro)
        if not check_barcode:
            all_files = []

        else:
            files_copy = [files_list[0], files_list[1]]
            if len(all_files) == 3:
                files_copy = all_files
                os.makedirs(os.path.join(path, "protocolar"), exist_ok=True)
                for arq in files_copy:
                    arq = str(arq)
                    barra = "\\" if "\\" in arq else "/"
                    fileN = arq.split(barra)[-1]
                    shutil.copy(arq, os.path.join(path, "protocolar", fileN))
                
    return all_files