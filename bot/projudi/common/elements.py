class elements_projudi:
    
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
        url_login = ""
        campo_username: str = ''
        campo_passwd: str = ''
        btn_entrar: str = ""
        
        url_busca: str = ""
        btn_busca: str = ""
        
    class AC:
        url_login = ""
        campo_passwd: str = ''
        btn_entrar: str = ""
        
        url_busca: str = ""
        btn_busca: str = ""
        
    class AM:
        url_login = "https://projudi.tjam.jus.br/projudi/usuario/logon.do?actionType=inicio"
        campo_username = '#login'
        campo_passwd: str = '#senha'
        btn_entrar: str = '#btEntrar'
        
        url_busca: str = "https://projudi.tjam.jus.br/projudi/processo/buscaProcessosQualquerInstancia.do?actionType=pesquisar"
        btn_busca: str = ""
        