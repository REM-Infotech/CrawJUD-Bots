class elements_elaw:
    
    url_login: str = ""
    campo_username: str = ''
    campo_passwd: str = ''
    btn_entrar: str = ""
    
    url_busca: str = ""
    btn_busca: str = ""
    
    class AME:
        url_login = ""
        campo_username = ''
        campo_passwd = ''
        btn_entrar = ''
        chk_login = ''
        
        url_busca = ""
        btn_busca = ""
    
    def __init__(self, state: str) -> None:
        
        # Mapeia os estados às classes correspondentes
        state_classes: dict[str, self.AC | self.AM | self.SP] = {
            "SP": self.SP,
            "AC": self.AC,
            "AM": self.AM
        }
        
        # Se o estado passado existir no dicionário, atualiza as variáveis
        state_class = state_classes[state].__dict__.copy()

        for func, name in self.AM.__dict__.items():
            if not func.startswith('__'):
                setattr(self, func, name)
                print(f"{func}: {name}")

    # Classes internas para diferentes estados
