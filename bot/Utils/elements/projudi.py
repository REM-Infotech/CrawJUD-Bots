class SP:
    url_login = ""
    campo_username = ""
    campo_passwd = ""
    btn_entrar = ""

    url_busca = ""
    btn_busca = ""


class AC:
    url_login = ""
    url_busca = ""
    btn_busca = ""


class AM:

    url_login = "https://projudi.tjam.jus.br/projudi/usuario/logon.do?actionType=inicio"
    campo_username = "#login"
    campo_passwd = "#senha"
    btn_entrar = "#btEntrar"
    chk_login = 'iframe[name="userMainFrame"]'

    url_busca = "https://projudi.tjam.jus.br/projudi/processo/buscaProcessosQualquerInstancia.do?actionType=pesquisar"
    btn_busca = ""

    btn_partes = "#tabItemprefix2"
    btn_infogeral = "#tabItemprefix0"
    includeContent = "includeContent"

    infoproc = 'table[id="informacoesProcessuais"]'
    assunto_proc = 'a[class="definitionAssuntoPrincipal"]'
    resulttable = "resultTable"
