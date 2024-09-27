# Importações necessárias
from datetime import datetime
import pytz
import pathlib
import os
from typing import Type
import base64
import sys
import subprocess
import platform
from time import sleep
from tqdm import tqdm
import sys
from clear import clear
import openpyxl
from socketio import Client
import logging
import json
from bot.head.Tools.PrintLogs.socketio import socket_message, disconnect_socket

# Define a codificação de caracteres como UTF-8
codificacao = 'utf-8'
mensagens = []


class printtext:
    
    def __init__(self, pid, row = 0):
        
        self.pid = pid
        self.row = row

    def print_log(self, type: str = None, message: str = None) -> str:
        try:
            return "ok"
        finally:
            prompt = f"({self.pid}, {type}, pos:{self.row}, {datetime.now(pytz.timezone('Etc/GMT+4')).strftime('%H:%M:%S')}) {message}"
            tqdm.write(prompt)
            socket_message(str(self.pid), prompt)
            mensagens.append(prompt)
            self.list_messages = mensagens
            if "fim da execução" in message.lower():
                sleep(1)
                disconnect_socket()
                self.file_log()

    def file_log(self):

        try:
            savelog = os.path.join(os.getcwd(), 'Temp' , self.pid, f'LogFile - PID {self.pid}.txt')
            with open(savelog.encode("utf-8"), "a") as f:
                for mensagem in self.list_messages:
                    
                    if self.pid in mensagem:
                        f.write(f"{mensagem}\n")
                pass
            
        except Exception as e:
            # Aguarda 2 segundos
            sleep(2)

            # Registra o erro
            logging.error(f'Exception: {e}', exc_info=True)

            # Exibe o erro
            tqdm.write(f"{e}")

    
