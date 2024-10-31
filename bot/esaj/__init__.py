class esaj:

    bot = ""
    Master = ""

    def __init__(self, bot: str, Master):
        self.bot = bot
        self.Master = Master

    from .capa import capa
    from .emissao import emissao
    from .protocolo import protocolo
    from .busca_pags import busca_pags
    from .movimentacao import movimentacao
