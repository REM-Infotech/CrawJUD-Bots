import os
import multiprocessing
from app import db, app
from app.models import ThreadBots

import psutil
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
    def BotStarter(self):  # -> Hints:

        systems = {
            "pje": pje,
            "esaj": esaj,
            "elaw": elaw,
            "caixa": caixa,
            "projudi": projudi,
            "calculadoras": calculadoras,
        }

        return systems.get(self.system)

    # argv: str = None, botname: str = None
    def __init__(self, **kwrgs: dict[str, str]):
        self.kwrgs = kwrgs
        self.__dict__.update(kwrgs)

    def start(self) -> int:

        try:
            with app.app_context():

                bot = self.BotStarter
                pid = os.path.basename(self.path_args.replace(".json", ""))
                process = multiprocessing.Process(
                    target=bot,
                    kwargs=self.kwrgs,
                    name=f"{self.display_name} - {pid}",
                    daemon=True,
                )
                process.start()
                process_id = process.ident

                # Salva o ID no "banco de dados"
                add_thread = ThreadBots(pid=pid, processID=process_id)
                db.session.add(add_thread)
                db.session.commit()
                return 200

        except Exception as e:
            print(e)
            return 500

    def stop(self, processID: int, pid: str) -> None:

        try:

            sinalizacao = f"{pid}.flag"
            processo = psutil.Process(processID)
            path_flag = os.path.join(os.getcwd(), "Temp", pid, sinalizacao)
            with open(path_flag, "w") as f:
                f.write("Encerrar processo")

            processo.wait(60)

            return f"Process {processID} stopped!"

        except psutil.TimeoutExpired:
            return "O processo não foi encerrado dentro do tempo limite"

        except psutil.NoSuchProcess:
            return f"Process {processID} stopped!"
