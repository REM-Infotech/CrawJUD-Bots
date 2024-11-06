class Configuracao:
    """Define propriedades específicas para cada elemento esperado."""

    def __init__(self, dados):
        self.dados = dados

    @property
    def url_login(self) -> str:
        return self.dados.get("url_login", "")

    @property
    def url_login_cert(self) -> str:
        return self.dados.get("url_login_cert", "")

    @property
    def campo_username(self) -> str:
        return self.dados.get("campo_username", "")

    @property
    def campo_passwd(self) -> str:
        return self.dados.get("campo_passwd", "")

    @property
    def btn_entrar(self) -> str:
        return self.dados.get("btn_entrar", "")

    @property
    def chk_login(self) -> str:
        return self.dados.get("chk_login", "")

    def __getattr__(self, name: str) -> str:

        prpt = self.dados.get(name)
        return prpt
