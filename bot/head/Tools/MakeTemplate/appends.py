from typing import Any


class listas:
    
    def __init__(self) -> None:
        pass
    
    def __call__(self, name_list: str) -> list[str]:
        
        self.lista = getattr(self, name_list, None)
        list = None
        if self.lista:
            list = self.lista()
            
        return list
    
    def cadastro_erro(self) -> list[str]:
        return ["Erro", "AREA_DIREITO", "SUBAREA_DIREITO", "ESTADO", "COMARCA", "FORO",
                "VARA", "DATA_DISTRIBUICAO", "PARTE_CONTRARIA", "TIPO_PARTE_CONTRARIA", "DOC_PARTE_CONTRARIA",
                "EMPRESA", "TIPO_EMPRESA", "DOC_EMPRESA", "UNIDADE_CONSUMIDORA", "CAPITAL_INTERIOR",
                "DIVISAO", "ACAO", "DATA_CITACAO", "OBJETO", "PROVIMENTO", "ADVOGADO_INTERNO",
                "ADV_PARTE_CONTRARIA", "FATO_GERADOR", "ESCRITORIO_EXTERNO", "VALOR_CAUSA", "FASE"
                ]


    def caixa_guias_emissao_sucesso(self) -> list[str]:
        return ['Descrição do Prazo', 'Valor do documento', "Data para pagamento",
                'Tipo de pagamento', 'Solicitante', 'Condenação', 'Código de Barras', 'Nome Documento']


    def esaj_guias_emissao_sucesso(self) -> list[str]:
        return ['Tipo Guia', 'Valor do documento', "Data para pagamento",
                'Tipo de pagamento', 'Solicitante', 'Condenação', 'Código de Barras', 'Nome Documento']


    def capa_sucesso(self) -> list[str]:

        return ["AREA_DIREITO", "SUBAREA_DIREITO", "ESTADO", "COMARCA", "FORO",
                "VARA", "DATA_DISTRIBUICAO", "PARTE_CONTRARIA", "TIPO_PARTE_CONTRARIA", "DOC_PARTE_CONTRARIA",
                "EMPRESA", "TIPO_EMPRESA", "DOC_EMPRESA", "ACAO", "ADVOGADO_INTERNO",
                "ADV_PARTE_CONTRARIA", "ESCRITORIO_EXTERNO", "VALOR_CAUSA"]

    def movimentacao_sucesso(self) -> list[str]:

        return ["Data movimentação", "Nome Movimentação", "Texto da movimentação", "Nome peticionante", "Classiicação Peticionante"]
        
    def sucesso(self) -> list[str]:
        
        return ["Mensagem de conclusão", "Nome Comprovante"]

    def erro(self) -> list[str]:

        return ['Motivo Erro']
