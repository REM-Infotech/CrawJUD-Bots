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
