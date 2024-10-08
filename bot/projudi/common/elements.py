from typing import Any

class elements_projudi:
    
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
        url_login = "https://projudi.tjam.jus.br/projudi/usuario/logon.do?actionType=inicio"
        campo_username = '#login'
        campo_passwd = '#senha'
        btn_entrar = '#btEntrar'
        chk_login = 'iframe[name="userMainFrame"]'
        
        url_busca = "https://projudi.tjam.jus.br/projudi/processo/buscaProcessosQualquerInstancia.do?actionType=pesquisar"
        btn_busca = ""
        
        btn_partes = '#tabItemprefix2'
        btn_infogeral = '#tabItemprefix0'
        includeContent = "includeContent"

        infoproc = 'table[id="informacoesProcessuais"]'
        assunto_proc = 'a[class="definitionAssuntoPrincipal"]'
        resulttable = "resultTable"
        
    def __init__(self, state: str) -> None:
        
        # Mapeia os estados às classes correspondentes
        state_classes: dict[str, Any] = {
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
    
        
        