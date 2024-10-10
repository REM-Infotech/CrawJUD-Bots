from typing import Union, Any


class elements_esaj:
    
    class SP:
        
        get_page_custas_pagas = 'button[class="btn btn-secondary btn-space linkConsultaSG"]'
        
        url_login = "https://consultasaj.tjam.jus.br/sajcas/login"
        url_login_cert = "https://consultasaj.tjam.jus.br/sajcas/login#aba-certificado"
        
        consultaproc_grau1 = 'https://consultasaj.tjam.jus.br/cpopg/open.do'
        consultaproc_grau2 = 'https://consultasaj.tjam.jus.br/cposgcr/'
        campo_username = ''
        campo_passwd = ''
        btn_entrar = ''
        chk_login = ''
        
        url_busca = ""
        btn_busca = ""
        
        acao = 'span[id="classeProcesso"]'
        vara_processual = 'span[id="varaProcesso"]'
        area_selecao = 'tablePartesPrincipais'
        id_valor = 'valorAcaoProcesso'
        data_processual = 'dataHoraDistribuicaoProcesso'
        classe_processual = '//*[@id="classeProcesso"]/span'
        selecao_processual = '//*[@id="secaoProcesso"]/span'
        orgao_processual = '//*[@id="orgaoJulgadorProcesso"]'
        status_processual = 'span[id="situacaoProcesso"]'
        relator = '//*[@id="relatorProcesso"]'
        
        nome_foro = 'input[name="entity.nmForo"]'
        tree_selection = 'input[name="classesTreeSelection.text"]'
        civil_selector = 'input[name="entity.flArea"][value="1"]'
        valor_acao = 'input[name="entity.vlAcao"]'
        botao_avancar = 'input[name="pbAvancar"]'
        interessado = 'input[name="entity.nmInteressado"]'
        check = 'input[class="checkg0r0"]'
        botao_avancar_dois = 'input[value="Avançar"]'
        boleto = 'a[id="linkBoleto"]'
        mensagem_retorno = 'td[id="mensagemRetorno"]'
        movimentacoes = 'tbody[id="tabelaTodasMovimentacoes"]'
        ultimas_movimentacoes = 'tabelaUltimasMovimentacoes'
        editar_classificacao = 'botaoEditarClassificacao'
        selecionar_classe = 'div.ui-select-container[input-id="selectClasseIntermediaria"]'
        toggle = 'span.btn.btn-default.form-control.ui-select-toggle'
        input_classe = 'input#selectClasseIntermediaria'
        select_categoria = 'div.ui-select-container[input-id="selectCategoria"]'
        input_categoria = 'input#selectCategoria'
        selecionar_grupo = './/li[@class="ui-select-choices-group"]/ul/li/span'
        input_documento = '#botaoAdicionarDocumento > input[type=file]'
        documento = '//nav[@class="document-data__nav"]/div/ul/li[5]/button[2]'
        processo_view = 'div[ui-view="parteProcessoView"]'
        nome = 'span[ng-bind="parte.nome"]'
        botao_incluir_peticao = 'button[ng-click="incluirParteDoProcessoPeticaoDiversa(parte)"]'
        botao_incluir_partecontraria = 'button[ng-click="incluirParteDoProcessoNoPoloContrario(parte)"]'
        parte_view = 'div[ui-view="parteView"]'
        botao_protocolar = '//*[@id="botaoProtocolar"]'
        botao_confirmar = 'div.popover-content button.confirm-button'
        botao_recibo = 'button[ng-click="consultarReciboPeticao(peticao)"]'
        
    class AC:
        
        get_page_custas_pagas = 'button[class="btn btn-secondary btn-space linkConsultaSG"]'
        
        url_login = "https://consultasaj.tjam.jus.br/sajcas/login"
        url_login_cert = "https://consultasaj.tjam.jus.br/sajcas/login#aba-certificado"
        campo_username = ''
        campo_passwd = ''
        btn_entrar = ''
        chk_login = ''
        
        url_busca = ""
        btn_busca = ""
        
        acao = 'span[id="classeProcesso"]'
        vara_processual = 'span[id="varaProcesso"]'
        area_selecao = 'tablePartesPrincipais'
        id_valor = 'valorAcaoProcesso'
        data_processual = 'dataHoraDistribuicaoProcesso'
        classe_processual = '//*[@id="classeProcesso"]/span'
        selecao_processual = '//*[@id="secaoProcesso"]/span'
        orgao_processual = '//*[@id="orgaoJulgadorProcesso"]'
        status_processual = 'span[id="situacaoProcesso"]'
        relator = '//*[@id="relatorProcesso"]'
        
        nome_foro = 'input[name="entity.nmForo"]'
        tree_selection = 'input[name="classesTreeSelection.text"]'
        civil_selector = 'input[name="entity.flArea"][value="1"]'
        valor_acao = 'input[name="entity.vlAcao"]'
        botao_avancar = 'input[name="pbAvancar"]'
        interessado = 'input[name="entity.nmInteressado"]'
        check = 'input[class="checkg0r0"]'
        botao_avancar_dois = 'input[value="Avançar"]'
        boleto = 'a[id="linkBoleto"]'
        mensagem_retorno = 'td[id="mensagemRetorno"]'
        movimentacoes = 'tbody[id="tabelaTodasMovimentacoes"]'
        ultimas_movimentacoes = 'tabelaUltimasMovimentacoes'
        editar_classificacao = 'botaoEditarClassificacao'
        selecionar_classe = 'div.ui-select-container[input-id="selectClasseIntermediaria"]'
        toggle = 'span.btn.btn-default.form-control.ui-select-toggle'
        input_classe = 'input#selectClasseIntermediaria'
        select_categoria = 'div.ui-select-container[input-id="selectCategoria"]'
        input_categoria = 'input#selectCategoria'
        selecionar_grupo = './/li[@class="ui-select-choices-group"]/ul/li/span'
        input_documento = '#botaoAdicionarDocumento > input[type=file]'
        documento = '//nav[@class="document-data__nav"]/div/ul/li[5]/button[2]'
        processo_view = 'div[ui-view="parteProcessoView"]'
        nome = 'span[ng-bind="parte.nome"]'
        botao_incluir_peticao = 'button[ng-click="incluirParteDoProcessoPeticaoDiversa(parte)"]'
        botao_incluir_partecontraria = 'button[ng-click="incluirParteDoProcessoNoPoloContrario(parte)"]'
        parte_view = 'div[ui-view="parteView"]'
        botao_protocolar = '//*[@id="botaoProtocolar"]'
        botao_confirmar = 'div.popover-content button.confirm-button'
        botao_recibo = 'button[ng-click="consultarReciboPeticao(peticao)"]'
        
    class AM:
        get_page_custas_pagas = 'button[class="btn btn-secondary btn-space linkConsultaSG"]'
        
        url_login = "https://consultasaj.tjam.jus.br/sajcas/login"
        url_login_cert = "https://consultasaj.tjam.jus.br/sajcas/login#aba-certificado"
        campo_username = ''
        campo_passwd = ''
        btn_entrar = ''
        chk_login = ''
        
        url_busca = ""
        btn_busca = ""
        
        acao = 'span[id="classeProcesso"]'
        vara_processual = 'span[id="varaProcesso"]'
        area_selecao = 'tablePartesPrincipais'
        id_valor = 'valorAcaoProcesso'
        data_processual = 'dataHoraDistribuicaoProcesso'
        classe_processual = '//*[@id="classeProcesso"]/span'
        selecao_processual = '//*[@id="secaoProcesso"]/span'
        orgao_processual = '//*[@id="orgaoJulgadorProcesso"]'
        status_processual = 'span[id="situacaoProcesso"]'
        relator = '//*[@id="relatorProcesso"]'
        
        nome_foro = 'input[name="entity.nmForo"]'
        tree_selection = 'input[name="classesTreeSelection.text"]'
        civil_selector = 'input[name="entity.flArea"][value="1"]'
        valor_acao = 'input[name="entity.vlAcao"]'
        botao_avancar = 'input[name="pbAvancar"]'
        interessado = 'input[name="entity.nmInteressado"]'
        check = 'input[class="checkg0r0"]'
        botao_avancar_dois = 'input[value="Avançar"]'
        boleto = 'a[id="linkBoleto"]'
        mensagem_retorno = 'td[id="mensagemRetorno"]'
        movimentacoes = 'tbody[id="tabelaTodasMovimentacoes"]'
        ultimas_movimentacoes = 'tabelaUltimasMovimentacoes'
        editar_classificacao = 'botaoEditarClassificacao'
        selecionar_classe = 'div.ui-select-container[input-id="selectClasseIntermediaria"]'
        toggle = 'span.btn.btn-default.form-control.ui-select-toggle'
        input_classe = 'input#selectClasseIntermediaria'
        select_categoria = 'div.ui-select-container[input-id="selectCategoria"]'
        input_categoria = 'input#selectCategoria'
        selecionar_grupo = './/li[@class="ui-select-choices-group"]/ul/li/span'
        input_documento = '#botaoAdicionarDocumento > input[type=file]'
        documento = '//nav[@class="document-data__nav"]/div/ul/li[5]/button[2]'
        processo_view = 'div[ui-view="parteProcessoView"]'
        nome = 'span[ng-bind="parte.nome"]'
        botao_incluir_peticao = 'button[ng-click="incluirParteDoProcessoPeticaoDiversa(parte)"]'
        botao_incluir_partecontraria = 'button[ng-click="incluirParteDoProcessoNoPoloContrario(parte)"]'
        parte_view = 'div[ui-view="parteView"]'
        botao_protocolar = '//*[@id="botaoProtocolar"]'
        botao_confirmar = 'div.popover-content button.confirm-button'
        botao_recibo = 'button[ng-click="consultarReciboPeticao(peticao)"]'
        
    # Mapeia os estados às classes correspondentes
    classes: dict[str, Union[SP, AC, AM]] = {
        "SP": SP,
        "AC": AC,
        "AM": AM
    }    
    
    def __init__(self, state: str) -> Union[SP, AC, AM]:
        
        # Se o estado passado existir no dicionário, atualiza as variáveis
        self.state_class: Union[elements_esaj.SP,\
            elements_esaj.AC, elements_esaj.AM] = self.classes[state]

                
    def __call__(self, *args, **kwds) -> Union[SP, AC, AM]:
        """"""
        return self.state_class
        
    def __getattr__(self, nome_do_atributo: str) -> Any:
        item = getattr(self.state_class, nome_do_atributo, None)
        if not item:
            raise AttributeError(f"Atributo '{nome_do_atributo}' não encontrado na classe '{self.state_class.__name__}'")
        return item
