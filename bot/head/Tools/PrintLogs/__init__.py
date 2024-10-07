# Importações necessárias
import os
import pytz
import logging
from tqdm import tqdm
from time import sleep
from datetime import datetime

from bot.head import CrawJUD
from bot.head.Tools.PrintLogs.socketio import socket_message, disconnect_socket

# Define a codificação de caracteres como UTF-8
codificacao = 'utf-8'
mensagens = []


class printtext(CrawJUD):
    
    def __init__(self, Head: CrawJUD, message: str):
        self.__dict__ = Head.__dict__.copy()
        
    def __call__(self) -> str:
        
        prompt = f"({self.pid}, {self.type_log}, pos:{self.row}, {datetime.now(pytz.timezone('Etc/GMT+4')).strftime('%H:%M:%S')}) {self.message}"
        tqdm.write(prompt)
        socket_message(self.pid, prompt, self.url_socket, self.type_log, self.row)
        mensagens.append(prompt)
        self.list_messages = mensagens
        if "fim da execução" in self.message.lower():
            sleep(1)
            disconnect_socket()
            self.file_log()
            

    def file_log(self):

        try:
            savelog = os.path.join(os.getcwd(), 'Temp' , self.pid, f'LogFile - PID {self.pid}.txt')
            with open(savelog, "a") as f:
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

    
