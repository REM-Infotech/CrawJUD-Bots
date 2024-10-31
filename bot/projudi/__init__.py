class projudi:
    
    from .capa import capa
    from .protocolo import protocolo
    from .proc_parte import proc_parte
    from .movimentacao import movimentacao
    
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
        
    
