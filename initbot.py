
from app import db, app
from flask import Flask

import os
import sys
import json
import time
import pathlib
import threading
import subprocess
from app.models import ThreadBots

class WorkerThread:
    
    def __init__(self) -> None:
        
        from bot import CrawJUD
        self.thread = None
        self.thread_id = None
        self.crawjud = CrawJUD
        
    def start(self, argv: str = None, botname: str= None) -> int:
        
        try:
            with app.app_context():
                
                pid = os.path.basename(argv.replace(".json", ""))
                
                self.thread = threading.Thread(target=self.run , args=(
                    app, argv, pid,), name=f"{botname} - {pid}")
                self.thread.start()
                self.thread_id = self.thread.ident  # Salva o ID da thread

                # Salva o ID no "banco de dados"
                add_thread = ThreadBots(
                    pid = pid,
                    thread_id=self.thread_id
                )
                db.session.add(add_thread)
                db.session.commit()
                return 200
        
        except Exception as e:
            print(e)
            return 500

    def run(self, app: Flask, path_args: str = None, pid: str = None):
        
        while not self.thread_id:
            print("wait pid thread") 
        with app.app_context():
            bot = self.crawjud(self)
            bot.setup(app, path_args)
        
    def stop(self) -> None:
        
        for thread in threading.enumerate():
            if thread.ident == self.thread_id:
                thread = thread
                thread._is_stopped = True  # Aciona o evento para parar a execução
                if thread is not None:
                    thread.join()
                    print(f"Thread {self.thread_id} finalizada")
                break
