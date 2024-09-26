def cadastro_erro() -> list:
    return ["Erro", "AREA_DIREITO", "SUBAREA_DIREITO", "ESTADO", "COMARCA", "FORO",
            "VARA", "DATA_DISTRIBUICAO", "PARTE_CONTRARIA", "TIPO_PARTE_CONTRARIA", "DOC_PARTE_CONTRARIA",
            "EMPRESA", "TIPO_EMPRESA", "DOC_EMPRESA", "UNIDADE_CONSUMIDORA", "CAPITAL_INTERIOR",
            "DIVISAO", "ACAO", "DATA_CITACAO", "OBJETO", "PROVIMENTO", "ADVOGADO_INTERNO",
            "ADV_PARTE_CONTRARIA", "FATO_GERADOR", "ESCRITORIO_EXTERNO", "VALOR_CAUSA", "FASE"
            ]


def caixa_guias_emissao_sucesso() -> list:
    return ['Descrição do Prazo', 'Valor do documento', "Data para pagamento",
            'Tipo de pagamento', 'Solicitante', 'Condenação', 'Código de Barras', 'Nome Documento']


def esaj_guias_emissao_sucesso() -> list:
    return ['Tipo Guia', 'Valor do documento', "Data para pagamento",
            'Tipo de pagamento', 'Solicitante', 'Condenação', 'Código de Barras', 'Nome Documento']


def capa_sucesso() -> list:

    return ["AREA_DIREITO", "SUBAREA_DIREITO", "ESTADO", "COMARCA", "FORO",
            "VARA", "DATA_DISTRIBUICAO", "PARTE_CONTRARIA", "TIPO_PARTE_CONTRARIA", "DOC_PARTE_CONTRARIA",
            "EMPRESA", "TIPO_EMPRESA", "DOC_EMPRESA", "ACAO", "ADVOGADO_INTERNO",
            "ADV_PARTE_CONTRARIA", "ESCRITORIO_EXTERNO", "VALOR_CAUSA"]

def movimentacao_sucesso() -> list:

    return ["Data movimentação", "Nome Movimentação", "Texto da movimentação", "Nome peticionante", "Classiicação Peticionante"]
    
def sucesso() -> list:
    
    return ["Mensagem de conclusão", "Nome Comprovante"]

def erro() -> list:

    return ['Motivo Erro']
