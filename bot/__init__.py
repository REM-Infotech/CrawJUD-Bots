import os
import multiprocessing
from app import db, app
from flask import Flask
from app.models import ThreadBots

from typing import Union

# Bots
from .pje import pje
from .esaj import esaj
from .elaw import elaw
from .caixa import caixa
from .projudi import projudi
from .calculadoras import calculadoras

Hints = Union[pje, esaj, elaw, caixa, projudi, calculadoras]


class WorkerThread:

    @property
    def BotStarter(self) -> Hints:

        systems = {
            "pje": pje,
            "esaj": esaj,
            "elaw": elaw,
            "caixa": caixa,
            "projudi": projudi,
            "calculadoras": calculadoras,
        }

        return systems.get(self.bot)

    # argv: str = None, botname: str = None
    def __init__(self, **kwrgs):
        self.__dict__.update(kwrgs)

    def start(self) -> int:

        try:
            with app.app_context():

                bot = self.BotStarter
                pid = os.path.basename(self.argv.replace(".json", ""))
                process = multiprocessing.Process(
                    target=bot(),
                    args=(
                        app,
                        self.argv,
                        pid,
                    ),
                    name=f"{self.botname} - {pid}",
                    daemon=True
                )
                process.start()
                process_id = process.ident

                # Salva o ID no "banco de dados"
                add_thread = ThreadBots(pid=pid, thread_id=process_id)
                db.session.add(add_thread)
                db.session.commit()
                return 200

        except Exception as e:
            print(e)
            return 500

    def run(self, app: Flask, path_args: str = None, pid: str = None):

        while not self.thread_id:
            print(f"wait {pid} thread".upper())

        with app.app_context():
            bot = self.crawjud(self)
            bot.setup(app, path_args)

    def stop(self) -> None:

        for thread in multiprocessing.get:
            if thread.ident == self.thread_id:
                thread = thread
                thread._is_stopped = True  # Aciona o evento para parar a execução
                if thread is not None:
                    thread.join()
                    print(f"Thread {self.thread_id} finalizada")
                break
