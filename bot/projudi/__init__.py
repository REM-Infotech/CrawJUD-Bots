from bot.projudi.capa import capa
from bot.projudi.protocolo import protocolo
from bot.projudi.movimentacao import movimentacao


def projudi(bot: str, Master):
    
    func = globals().get(bot)
    return func(Master)
    
