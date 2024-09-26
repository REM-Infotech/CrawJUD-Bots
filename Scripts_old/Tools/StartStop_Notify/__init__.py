from app import db
from app import app
from app.models import ExecutionsTable

import os
from typing import Type
import logging
import platform
from clear import clear
from datetime import datetime
import pytz
from time import sleep
import json

from Scripts.Tools.ClearCache import DelCache
from Scripts.Tools.StartStop_Notify.uninstall_cert import uninstall
from Scripts.Tools.StartStop_Notify.makefile import makezip
from Scripts.Tools.StartStop_Notify.upload_zip import enviar_arquivo_para_gcs
from Scripts.Tools.StartStop_Notify.send_email import email_stop, email_start


url_cache = []

def url_socket(pid) -> str:
    
    
    if len(url_cache) > 0:
        return url_cache[0]
    
    with app.app_context():
        
        sleep(5)
        
        url_Server = ExecutionsTable.query.filter_by(pid=pid).first()
        url_srv = url_Server.url_socket
        
        db.session.close()
    
    url_cache.append(url_srv)
    return url_srv


class SetStatus():
    
    def send_total_rows(self, rows, pid):
        
        try:
            socket_address = url_socket(pid)
                
            with app.app_context():
                QueryLogs = ExecutionsTable.query.filter_by(pid=pid).first()
                QueryLogs.total_rows = rows
                QueryLogs.url_socket = socket_address
                db.session.commit()
                db.session.close()
                
        except Exception as e:
            logging.error(f'Exception: {e}', exc_info=True)
        
    def botstart(self, status):
        
        try:
            with app.app_context():

                InsertExecution = ExecutionsTable.query.filter_by(pid=status[1]).first()
                
                if platform.system() == "Windows":
                    
                    status[4] = str(status[4]).split("\\")[-1]
                
                InsertExecution.data_execucao = datetime.now(pytz.timezone('Etc/GMT+4'))
                InsertExecution.file_output = "Arguardando Arquivo"
                InsertExecution.arquivo_xlsx = status[4]  
                InsertExecution.status = status[3]
                
                try:
                    db.session.commit()
                    db.session.close()
                    
                except Exception as e:
                    print(e)
            
            email_start(status)
            
        except Exception as e:
            logging.error(f'Exception: {e}', exc_info=True)   
    
    def botstop(self, status):
        
        try:
            
            if platform.system() == "Windows" and "esaj" in status[2] and "peticionamento" in status[2]:
                
                json_args = os.path.join(os.getcwd(), "Temp", status[1], f"args_{status[1]}.json")
                
                with open(json_args, "rb") as file:
                    
                    arg = json.load(file)["login"]

                try:
                    uninstall(arg)
                except Exception as e:
                    print(e)
            
            zip_file = makezip(status)
            
            path_output = os.path.join(os.getcwd(), zip_file)
            
            if os.path.exists(path_output):
                
                arquivo_local = path_output

                objeto_destino = path_output.split("/")[-1]
                
            
            enviar_arquivo_para_gcs(arquivo_local, objeto_destino)
            
            try:
                email_stop(status)
            
            except Exception as e:
                print(e)
            
            with app.app_context():
                try:
                    UpdateTable = ExecutionsTable.query.filter_by(pid=status[1]).first()
                    
                except Exception as e:
                    print(e)
                    
                UpdateTable.status = status[3]
                UpdateTable.file_output = objeto_destino
                UpdateTable.data_finalizacao = datetime.now(pytz.timezone('Etc/GMT+4'))
                db.session.commit()
                db.session.close()
        
            DelCache().clear(status[1])
            
            clear()
            
        except Exception as e:
            logging.error(f'Exception: {e}', exc_info=True)
            
    

# Substitua os valores abaixo pelos seus próprios dados
nome_do_bucket = 'seu-bucket'





