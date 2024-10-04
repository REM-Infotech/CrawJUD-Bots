

class esaj:
    from bot.esaj.capa import capa
    from bot.esaj.emissao import emissao
    from bot.esaj.protocolo import protocolo
    from bot.esaj.busca_pags import busca_pags
    from bot.esaj.movimentacao import movimentacao
    def __init__(self, bot: str, Master) -> (capa | emissao | protocolo | busca_pags | movimentacao):
        
        func = globals().get(bot)
        return func(Master)
        
from bot.esaj.common.elements import elements_esaj