from typing import Union, Any

class elements_caixa:
    
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
        
    classes: dict[str, Union[SP, AC, AM]] = {
        "SP": SP,
        "AC": AC,
        "AM": AM
    }    
    
    def __init__(self, state: str) -> Union[SP, AC, AM]:
        
        # Se o estado passado existir no dicionário, atualiza as variáveis
        self.state_class: Union[elements_caixa.SP,\
            elements_caixa.AC, elements_caixa.AM] = self.classes[state]

                
    def __call__(self, *args, **kwds) -> Union[SP, AC, AM]:
        return self.state_class
        
    def __getattr__(self, nome_do_atributo: str) -> Any:
        item = getattr(self.state_class, nome_do_atributo, None)
        if not item:
            raise AttributeError(f"Atributo '{nome_do_atributo}' não encontrado na classe '{self.state_class.__name__}'")
        return item
