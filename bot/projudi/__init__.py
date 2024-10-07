

class projudi:
    
    from bot.projudi.capa import capa
    from bot.projudi.protocolo import protocolo
    from bot.projudi.movimentacao import movimentacao
    bot = ""
    Master = ""
    
    def __init__(self, bot: str, Master):
        self.bot = bot
        self.Master = Master
    
    def __call__(self) -> capa | protocolo | movimentacao:
        self.execution = globals().get(self.bot)(self.Master).execution()
    
from bot.projudi.common.elements import elements_projudi