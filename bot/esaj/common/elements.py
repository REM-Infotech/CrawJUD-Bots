from typing import Any


class elements_esaj:
    
    class SP:
        url_login = ""
        campo_username = ''
        campo_passwd = ''
        btn_entrar = ""
        
        url_busca = ""
        btn_busca = ""
        
    class AC:
        url_login = ""
        url_busca = ""
        btn_busca = ""
        
    class AM:
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
        state_class = state_classes[state]

        for func, name in state_class.__dict__.items():
            if not func.startswith('__'):
                setattr(self, func, name)

    # Classes internas para diferentes estados
