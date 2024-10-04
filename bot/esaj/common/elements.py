class elements_esaj:
    
    url_login: str = ""
    campo_username: str = ''
    campo_passwd: str = ''
    btn_entrar: str = ""
    
    url_busca: str = ""
    btn_busca: str = ""
    
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
        get_page_custas_pagas = 'button[class="btn btn-secondary btn-space linkConsultaSG"]'
        
        url_login = ""
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
        