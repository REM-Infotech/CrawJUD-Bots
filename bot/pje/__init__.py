class pje:
    
    bot = ""
    Master = ""
    
    def __init__(self, bot: str, Master):
        self.bot = bot
        self.Master = Master
    
    def __call__(self) -> None:
        try:
            self.execution: pauta = globals().get(self.bot)(self.Master)
            self.execution.execution()
            
        except Exception as e:
            print(e)
            raise e
        
from bot.pje.pauta import pauta
# from bot.pje.protocolo import protocolo
# from bot.pje.movimentacao import movimentacao
from bot.pje.common.elements import elements_pje