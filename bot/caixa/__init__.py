class caixa:
    
    bot = ""
    Master = ""
    
    def __init__(self, bot: str, Master):
        self.bot = bot
        self.Master = Master
    
    def __call__(self) -> None:
        try:
            self.execution = globals().get(self.bot)(self.Master)
            self.execution.execution()
            
        except Exception as e:
            print(e)
            raise e
        
from bot.caixa.emissao import emissao