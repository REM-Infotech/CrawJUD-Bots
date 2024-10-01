class elements_projudi:
    
    url_login: str = ""
    campo_username: str = ''
    campo_passwd: str = ''
    btn_entrar: str = ""
    
    url_busca: str = ""
    btn_busca: str = ""
    
    class SP:
        url_login = "https://consultasaj.tjam.jus.br/sajcas/login#aba-certificado"
        campo_username = '#usernameForm'
        campo_passwd = '#passwordForm'
        btn_entrar = ""
        
        url_busca = "url_de_busca_SP"
        btn_busca = "btn_busca_SP"
        
    class AC:
        url_login = "https://projudi.tjam.jus.br/projudi/processo/buscaProcessosQualquerInstancia.do?actionType=pesquisar"
        url_busca = "url_de_busca_AC"
        btn_busca = "btn_busca_AC"
        
    class AM:
        url_login = "https://projudi.tjam.jus.br/projudi/processo/buscaProcessosQualquerInstancia.do?actionType=pesquisar"
        campo_username = '#usernameForm'
        campo_passwd = '#passwordForm'
        btn_entrar = '//*[@id="pbEntrar"]'
        
        
        url_busca = "url_de_busca_AC"
        btn_busca = "btn_busca_AC"
    
    def __init__(self, state: str) -> None:
        
        # Mapeia os estados às classes correspondentes
        state_classes: dict[str, self.AC | self.AM | self.SP] = {
            "SP": self.SP,
            "AC": self.AC,
            "AM": self.AM
        }
        
        teste = self.AM..items()
        # Se o estado passado existir no dicionário, atualiza as variáveis
        state_class = state_classes[state].__dict__.copy()

        for func, name in state_classes[state].__dict__().items():
            setattr(self, func, name)
        
        return self

    # Classes internas para diferentes estados
    
        
        