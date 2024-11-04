from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

import os
import pytz
import logging
from tqdm import tqdm
from time import sleep
from datetime import datetime
from .socketio import SocketIo_CrawJUD
from dotenv import dotenv_values
from ...CrawJUD import CrawJUD
from app.default_config import SQLALCHEMY_DATABASE_URI

codificacao = "UTF-8"
mensagens = []

url_socket = dotenv_values().get("HOST")

# Crie o Engine com um pool de conexões ajustado (por exemplo, max 10 conexões)
engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_size=10, max_overflow=20)

# Configure o sessionmaker e o scoped_session
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)
session = Session()


class printtext(CrawJUD):

    message_error = None
    row = 0

    def __init__(self, **kwrgs):
        self.ioBot = SocketIo_CrawJUD(**kwrgs)
        self.__dict__.update(kwrgs)

    def print_msg(self):

        log = self.message
        if self.message_error:
            log = self.message_error
            self.message_error = None

        if self.row > 0:
            self.row -= 1

        self.prompt = f"({self.pid}, {self.type_log}, pos:{self.row}, {datetime.now(pytz.timezone('America/Manaus')).strftime('%H:%M:%S')}) {log}"
        tqdm.write(self.prompt)

        self.socket_message()
        mensagens.append(self.prompt)

        self.list_messages = mensagens
        if "fim da execução" in self.message.lower():
            sleep(1)
            self.file_log()

    def file_log(self) -> None:

        try:
            savelog = os.path.join(
                os.getcwd(), "Temp", self.pid, f"LogFile - PID {self.pid}.txt"
            )
            with open(savelog, "a") as f:
                for mensagem in self.list_messages:

                    if self.pid in mensagem:
                        f.write(f"{mensagem}\n")
                pass

        except Exception as e:
            # Aguarda 2 segundos
            sleep(2)

            # Registra o erro
            logging.error(f"Exception: {e}", exc_info=True)

            # Exibe o erro
            tqdm.write(f"{e}")

    def socket_message(self) -> None:

        chk_type1 = "fim da execução" in self.prompt
        chk_type2 = "falha ao iniciar" in self.prompt
        message_stop = [chk_type1, chk_type2]

        try:
            data: dict[str, str | int] = {
                "message": self.prompt,
                "pid": self.pid,
                "type": self.type_log,
                "pos": self.row,
                "graphicMode": self.graphicMode,
            }

            if any(message_stop):
                data.update({"system": self.system, "typebot": self.typebot})

            self.ioBot.send_message(data=data, url_socket=url_socket)

        except Exception as e:
            print(e)
