from app import db
from app import app

import os
import json
import pytz

import pathlib
import logging
import platform
import openpyxl
from time import sleep
from clear import clear
from typing import Type
from datetime import datetime
from werkzeug.datastructures import FileStorage

from app.models import Users, BotsCrawJUD, Executions
from openpyxl.worksheet.worksheet import Worksheet

url_cache = []
from bot.head.Tools.ClearCache import DelCache
from bot.head.Tools.StartStop_Notify.makefile import makezip
from bot.head.Tools.StartStop_Notify.uninstall_cert import uninstall
from bot.head.Tools.StartStop_Notify.upload_zip import enviar_arquivo_para_gcs
from bot.head.Tools.StartStop_Notify.send_email import email_stop, email_start



class SetStatus:
    
    
    
    def __init__(self, form: dict[str, str] = {}, files: dict[FileStorage] = {},
                 id: int  = None, system: str = None, type: str = None,
                 usr: str = None, pid: str = None, status: str = "Finalizado") -> str:
        
        if len(form):
            self.form = form
            
        if len(files):
            self.files = files
            
        self.id = id
        self.system = system
        self.type = type
        self.user = form.get("user", usr)
        self.pid = form.get("pid", pid)
        self.status = status
        
    def start_bot(self) -> str:
        
        path_pid = os.path.join(app.config["TEMP_PATH"], self.pid)
        os.makedirs(path_pid, exist_ok=True)
        
        for f, value in self.files.items():
            filesav = os.path.join(path_pid, f)
            value.save(filesav)
        
        data = {} 
        path_args = os.path.join(path_pid, f"{self.pid}.json")
        for key, value in self.form.items():
            data.update({key: value})
        
        data.update({
            "id": self.id,
            "system": self.system,
            "type": self.type
        })
        
        input_file = os.path.join(pathlib.Path(path_args).parent.resolve(), data['xlsx'])
        wb = openpyxl.load_workbook(filename=input_file)
        ws: Worksheet = wb.active
        rows = ws.max_row
        
        data.update({"total_rows": rows})
        
        with open(path_args, "w") as f:
            f.write(json.dumps(data))   
        
        execut = Executions(
            pid = self.pid,
            status = "Em Execução",
            arquivo_xlsx = data.get("xlsx"),
            url_socket = data.get("url_socket"),
            total_rows = rows,
            data_execucao = datetime.now(pytz.timezone('Etc/GMT+4')),
            file_output = "Arguardando Arquivo"
        )
        
        usr = Users.query.filter(Users.login == self.user).first()
        bt = BotsCrawJUD.query.filter(BotsCrawJUD.id == self.id).first()
        
        execut.user.append(usr)
        execut.bot.append(bt)
        
        db.session.add(execut)
        db.session.commit()
        
        try:
            email_start(usr, self.pid)
            
        except Exception as e:
            logging.error(f'Exception: {e}', exc_info=True)
            
        return path_args
    
    def botstop(self):
        
        try:
            srv = platform.system() in ("Windows")
            sys = self.system.lower() in ("esaj")
            typebot = self.type.lower() in ("protocolo")
            
            if all([srv, sys, typebot]):
                
                json_args = os.path.join(os.getcwd(), "Temp", self.pid, f"{self.pid}.json")
                with open(json_args, "rb") as f:
                    arg = json.load(f)["login"]

                try:
                    self.uninstall(arg)
                except Exception as e:
                    print(e)
            
            zip_file = makezip(self.pid)
            objeto_destino = os.path.basename(zip_file)
            enviar_arquivo_para_gcs(zip_file)
            
            
            execution = Executions.query.filter(Executions.pid == self.pid).first()
            
            try:
                email_stop(execution)
            except Exception as e:
                logging.error(f'Exception: {e}', exc_info=True)
            
                    
            execution.status = self.status
            execution.file_output = objeto_destino
            execution.data_finalizacao = datetime.now(pytz.timezone('Etc/GMT+4'))
            db.session.commit()
            db.session.close()
        
            DelCache(self.pid)

            
        except Exception as e:
            logging.error(f'Exception: {e}', exc_info=True)





