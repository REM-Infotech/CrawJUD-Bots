class elaw:
    
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
        
    from .download import download
    from .cadastro import cadastro
    from .pagamentos import sol_pags
    from .andamentos import andamentos
    from .complementar import complement
    from .provisionamento import provisao
    from .audiencia import audiencia as prazos
