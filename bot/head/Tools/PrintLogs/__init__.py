from app import io
# Importações necessárias
import os
import pytz
import logging
from tqdm import tqdm
from time import sleep
from datetime import datetime

from bot.head import CrawJUD

# Define a codificação de caracteres como UTF-8
codificacao = 'utf-8'
mensagens = []


class printtext(CrawJUD):
    
    def __init__(self, Head: CrawJUD):
        self.__dict__ = Head.__dict__.copy()
    
    def __call__(self, Head: CrawJUD):
        
        self.__dict__ = Head.__dict__.copy()
        self.log_message()
        
    def log_message(self) -> None:
        
        log = self.message
        if self.message_error:
            log = self.message_error
            
        self.prompt = f"({self.pid}, {self.type_log}, pos:{self.row}, {datetime.now(pytz.timezone('Etc/GMT+4')).strftime('%H:%M:%S')}) {log}"
        tqdm.write(self.prompt)
        
        self.socket_message()
        mensagens.append(self.prompt)
        
        self.list_messages = mensagens
        if "fim da execução" in self.message.lower():
            sleep(1)
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
    
    def socket_message(self):
    
        try:
            data = {'message': self.prompt,
                    'pid': self.pid, 
                    "type": self.type_log, 
                    "pos": self.row}
            
            self.emitMessage(data)
            
        except Exception as e:
            print(e)

    def emitMessage(self, data: dict[str, str]):
        
        with self.app.app_context():
            io.emit('log_message', data, namespace='/log')