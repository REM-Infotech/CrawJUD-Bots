from bot.projudi.capa import capa
from bot.projudi.protocolo import protocolo
from bot.projudi.movimentacao import movimentacao
from bot.projudi.common.elements import elements_projudi


def projudi(state: str, bot: str, Master):
    
    
    elementos = getattr(elements_projudi, state.upper())
    
    try:
        func = globals().get(bot)
        return func(Master)
    except Exception as e:
        print(e)
    
