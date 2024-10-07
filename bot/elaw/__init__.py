class elaw:
    
    from bot.elaw.download import download
    from bot.elaw.cadastro import cadastro
    from bot.elaw.pagamentos import sol_pags
    from bot.elaw.andamentos import andamentos
    from bot.elaw.complementar import complement
    from bot.elaw.provisionamento import provisao
    
    def __init__(self, bot: str, Master) -> (
        download | cadastro | sol_pags | andamentos | complement| provisao):
        
        func = globals().get(bot)
        return func(Master)
        
from bot.elaw.common.elements import elements_elaw
