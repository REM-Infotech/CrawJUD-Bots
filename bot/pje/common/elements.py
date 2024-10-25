from typing import Union, Any


class elements_pje:

    # Classes internas para diferentes estados
    class SP:
        url_login = "https://projudi.tjam.jus.br/projudi/processo/buscaProcessosQualquerInstancia.do?actionType=pesquisar"
        url_busca = "url_de_busca_SP"
        btn_busca = "btn_busca_SP"
        
    class AC:
        url_login = "https://projudi.tjam.jus.br/projudi/processo/buscaProcessosQualquerInstancia.do?actionType=pesquisar"
        url_busca = "url_de_busca_AC"
        btn_busca = "btn_busca_AC"
        
    class AM:
        url_login: str = "https://pje.trt11.jus.br/primeirograu/login.seam"
        chk_login: str = "https://pje.trt11.jus.br/pjekz/painel/usuario-externo"
        
        login_input: str = 'input[id="username"]'
        password_input: str = 'input[id="password"]'
        btn_entrar: str = 'button[id="btnEntrar"]'
        url_pautas: str = "https://pje.trt11.jus.br/consultaprocessual/pautas"
        
        url_busca: str = "url_de_busca_AC"
        btn_busca: str = "btn_busca_AC"
        
    classes: dict[str, Union[SP, AC, AM]] = {
        "SP": SP,
        "AC": AC,
        "AM": AM}
        
    def __init__(self, state: str) -> Union[SP, AC, AM]:
        
        # Se o estado passado existir no dicionário, atualiza as variáveis
        self.state_class = self.classes[state]

                
    def __call__(self, *args, **kwds) -> Union[SP, AC, AM]:
        """
        ### Retorna self.state_class
        
        #### self.state_class: Union[SP, AC, AM]
        
        """
        return self.state_class
        
    def __getattr__(self, nome_do_atributo: str) -> Any:
        item = getattr(self.state_class, nome_do_atributo, None)
        if not item:
            raise AttributeError(f"Atributo '{nome_do_atributo}' não encontrado na classe '{self.state_class.__name__}'")
        return item
