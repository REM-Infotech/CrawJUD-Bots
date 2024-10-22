from typing import Union

class elaw:
    
    bot = ""
    Master = ""
    
    def __init__(self, bot: str, Master):
        self.bot = bot
        self.Master = Master
    
    def __call__(self) -> None:
        try:
            self.execution: \
                Union[download, andamentos, prazos,
                      cadastro, complement,
                      provisao, sol_pags]\
                        = globals().\
                get(self.bot)(self.Master)
                
            self.execution.execution()
            
        except Exception as e:
            print(e)
            raise e

from bot.elaw.download import download
from bot.elaw.cadastro import cadastro
from bot.elaw.pagamentos import sol_pags
from bot.elaw.andamentos import andamentos
from bot.elaw.complementar import complement
from bot.elaw.provisionamento import provisao
from bot.elaw.audiencia import audiencia as prazos
from bot.elaw.common.elements import elements_elaw
