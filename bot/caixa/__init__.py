class caixa:
    
    bot = ""
    Master = ""
    
    def __init__(self, bot: str, Master):
        self.bot = bot
        self.Master = Master
    
    def __call__(self) -> None:
        try:
            
            self.execution = getattr(self, self.bot)(self.Master)
            self.execution.execution()
            
        except Exception as e:
            raise e
        
    from .emissao import emissao as emissor
    from .common.elements import elements_caixa
