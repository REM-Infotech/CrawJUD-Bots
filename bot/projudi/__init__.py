from bot.projudi.capa import capa
from bot.projudi.protocolo import protocolo
from bot.projudi.movimentacao import movimentacao


def projudi(bot: str, Master):
    
    try:
        func = globals().get(bot)
        return func(Master)
    except Exception as e:
        print(e)
    
