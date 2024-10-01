class elements_esaj:
    
    url_login: str = ""
    campo_username: str = ''
    campo_passwd: str = ''
    btn_entrar: str = ""
    
    url_busca: str = ""
    btn_busca: str = ""
    
    def __init__(self, state: str) -> None:
        
        # Mapeia os estados às classes correspondentes
        state_classes = {
            "SP": self.SP,
            "AC": self.AC,
            "AM": self.AM
        }
        
        # Se o estado passado existir no dicionário, atualiza as variáveis
        if state in state_classes:
            state_class = state_classes[state]()
            for attr_name, attr_value in state_class.__dict__.items():
                if not attr_name.startswith('__'):  # Ignora atributos internos
                    setattr(self, attr_name, attr_value)
        else:
            raise ValueError(f"Estado '{state}' não é válido.")

    # Classes internas para diferentes estados
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
        