from typing import ClassVar

class caixa:
    
    bot = ""
    Master = ""
    
    def __init__(self, bot: str, Master):
        self.bot = bot
        self.Master = Master
    
    def __call__(self) -> None:
        try:
            self.execution = globals().get(self.bot)
            if self.execution:
                self.execution(self.Master).execution()
            
        except Exception as e:
            print(e)
            raise e
        
from bot.caixa.emissao import emissao as emissor
from bot.caixa.common.elements import elements_caixa