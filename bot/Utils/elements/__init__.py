class ElementsBot:

    from .properties import Configuracao
    from .esaj import AM, AC, SP

    funcs = {
        "esaj": {"SP": SP, "AC": AC, "AM": AM},
        "projudi": {"SP": SP, "AC": AC, "AM": AM},
    }

    def __init__(self, state_or_client: str):
        self.locale = state_or_client

    @property
    def elements(self):
        """Retorna a configuração de acordo com o estado ou cliente."""
        dados = self.esaj_.get(self.locale, {})

        if not dados:
            raise AttributeError("Estado ou cliente não encontrado.")

        return self.Configuracao(dados.__dict__)
