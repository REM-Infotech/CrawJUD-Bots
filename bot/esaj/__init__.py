

class esaj:
    from bot.esaj.capa import capa
    from bot.esaj.emissao import emissao
    from bot.esaj.protocolo import protocolo
    from bot.esaj.busca_pags import busca_pags
    from bot.esaj.movimentacao import movimentacao
    bot = ""
    Master = ""
    
    def __init__(self, bot: str, Master):
        self.bot = bot
        self.Master = Master
    
    def __call__(self) -> capa | protocolo | movimentacao | busca_pags | emissao:
        self.execution = globals().get(self.bot)(self.Master).execution()
        
from bot.esaj.common.elements import elements_esaj