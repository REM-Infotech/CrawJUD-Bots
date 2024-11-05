class BaseElementsBot:

    from .properties import Configuracao
    from .esaj import ESAJ_AM
    from .projudi import PROJUDI_AM

    funcs = {
        "esaj": {"AM": ESAJ_AM},
        "projudi": {"AM": PROJUDI_AM},
    }

    def __init__(self, *args, **kwrgs):
        self.__dict__.update(kwrgs)

    @property
    def elements(self):
        """Retorna a configuração de acordo com o estado ou cliente."""
        dados = self.funcs.get(self.system_bot).get(self.state_or_client)

        if not dados:
            raise AttributeError("Estado ou cliente não encontrado.")

        return self.Configuracao(dados.__dict__)


class ElementsBot(BaseElementsBot):

    def __init__(self, *args, **kwrgs):
        super().__init__(*args, **kwrgs)
