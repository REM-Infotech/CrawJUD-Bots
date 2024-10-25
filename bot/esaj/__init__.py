class esaj:
    
    bot = ""
    Master = ""
    
    def __init__(self, bot: str, Master):
        self.bot = bot
        self.Master = Master
    
    def __call__(self) -> None:
        try:
            
            self.execution = getattr(self.bot)(self.Master)
            self.execution.execution()
            
        except Exception as e:
            print(e)
            raise e

    from bot.esaj.capa import capa
    from bot.esaj.emissao import emissao
    from bot.esaj.protocolo import protocolo
    from bot.esaj.busca_pags import busca_pags
    from bot.esaj.movimentacao import movimentacao
    from bot.esaj.common.elements import elements_esaj
