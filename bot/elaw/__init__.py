from bot.elaw.download import download
from bot.elaw.cadastro import cadastro
from bot.elaw.pagamentos import sol_pags
from bot.elaw.andamentos import andamentos
from bot.elaw.complementar import complement
from bot.elaw.provisionamento import provisao


def esaj(bot: str, Master):
    
    func = globals().get(bot)
    return func(Master)
    