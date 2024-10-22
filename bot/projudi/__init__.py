class projudi:
    
    bot = ""
    Master = ""
    
    def __init__(self, bot: str, Master):
        self.bot = bot
        self.Master = Master
    
    def __call__(self) -> None:
        try:
            self.execution: capa | protocolo | movimentacao = globals().\
                get(self.bot)(self.Master)
            self.execution.execution()
            
        except Exception as e:
            print(e)
            raise e
        
from bot.projudi.capa import capa
from bot.projudi.protocolo import protocolo
from bot.projudi.proc_parte import proc_parte
from bot.projudi.movimentacao import movimentacao
from bot.projudi.common.elements import elements_projudi