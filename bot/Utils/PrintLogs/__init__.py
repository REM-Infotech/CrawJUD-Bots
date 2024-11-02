""" bot.head.Tools.PrintLogs.py """

from app import db

# Importações necessárias
import os
import pytz
import logging
from tqdm import tqdm
from time import sleep
from datetime import datetime
from .socketio import SocketIo_CrawJUD
from app.models import CacheLogs, Executions
from dotenv import dotenv_values

# Define a codificação de caracteres como UTF-8
codificacao = "UTF-8"
mensagens = []

url_socket = dotenv_values().get("HOST")


class printtext:

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

            self.emitMessage(data)

        except Exception as e:
            print(e)

    def emitMessage(self, data: dict[str, str]):

        log_pid = CacheLogs.query.filter(CacheLogs.pid == self.pid).first()
        if not log_pid:

            execut = Executions.query.filter(Executions.pid == self.pid).first()
            log_pid = CacheLogs(
                pid=self.pid,
                pos=int(data["pos"]),
                total=int(execut.total_rows) - 1,
                remaining=int(execut.total_rows) - 1,
                success=0,
                errors=0,
                status=execut.status,
                last_log=data["message"],
            )
            db.session.add(log_pid)

        elif log_pid:

            log_pid.pos = int(data["pos"])

            type_S1 = data["type"] == "success"
            type_S2 = data["type"] == "info"
            type_S3 = data["graphicMode"] != "doughnut"

            typeSuccess = type_S1 or type_S2 and type_S3

            if typeSuccess:

                log_pid.remaining -= 1
                if "fim da execução" not in data["message"].lower():
                    log_pid.success += 1

                log_pid.last_log = data["message"]

            elif data["type"] == "error":

                log_pid.remaining -= 1
                log_pid.errors += 1
                log_pid.last_log = data["message"]

                if self.row == 0:
                    log_pid.errors = log_pid.total
                    log_pid.remaining = 0

            if "fim da execução" in data["message"].lower():
                log_pid.remaining = 0
                log_pid.status = "Finalizado"

        db.session.commit()
        data.update(
            {
                "pid": data["pid"],
                "pos": int(data["pos"]),
                "total": log_pid.total,
                "remaining": log_pid.remaining,
                "success": log_pid.success,
                "errors": log_pid.errors,
                "status": log_pid.status,
                "last_log": log_pid.last_log,
            }
        )

        self.ioBot.send_message(data=data, url_socket=url_socket)
