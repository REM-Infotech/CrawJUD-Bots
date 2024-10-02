from bot.esaj.capa import capa
from bot.esaj.emissao import emissao
from bot.esaj.protocolo import protocolo
from bot.esaj.busca_pags import busca_pags
from bot.esaj.movimentacao import movimentacao


def esaj(bot: str, Master):
    
    func = globals().get(bot)
    return func(Master)
    
