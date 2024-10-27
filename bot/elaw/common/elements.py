from typing import Union, Callable


class elements_elaw:
    
    class AME:
        
        class condenacao:
            string = ""
            
        class custas:
            
            string = ""
        
        ## Login Elaw
        url_login = ""
        campo_username = ''
        campo_passwd = ''
        btn_entrar = ''
        chk_login = ''
        
        ## Busca Elaw
        url_busca = ""
        btn_busca = ""
            
        ## Robô Lançar Audiências
        switch_pautaAndamento = 'a[href="#tabViewProcesso:agendamentosAndamentos"]'
        btn_NovaAudiencia = 'button[id="tabViewProcesso:novaAudienciaBtn"]'
        selectorTipoAudiencia = 'select[id="j_id_2l:comboTipoAudiencia_input"]'
        DataAudiencia = 'input[id="j_id_2l:j_id_2p_2_8_8:dataAudienciaField_input"]'
        btn_Salvar = 'button[id="btnSalvarNovaAudiencia"]'
        tablePrazos = 'tbody[id="tabViewProcesso:j_id_i3_4_1_3_d:dtAgendamentoResults_data"]'
        
        ## Robô cadastros
        numero_processo = "input[id='j_id_3k_1:j_id_3k_4_2_2_2_9_f_2:txtNumeroMask']"
        
        ## For Selectors
        estado_input = "select[id='j_id_3k_1:j_id_3k_4_2_2_1_9_u_1:comboEstadoVara_input']"
        comarca_input = "select[id='j_id_3k_1:j_id_3k_4_2_2_1_9_u_1:comboComarcaVara_input']"
        foro_input = "select[id='j_id_3k_1:j_id_3k_4_2_2_1_9_u_1:comboForoTribunal_input']"
        vara_input = "select[id='j_id_3k_1:j_id_3k_4_2_2_1_9_u_1:comboVara_input']"
        tipo_empresa_input = "select[id='j_id_3k_1:j_id_3k_4_2_2_4_9_2_5_input']"
        fase_input = 'select[id="j_id_3k_1:processoFaseCombo_input"]'
        provimento_input = 'select[id="j_id_3k_1:j_id_3k_4_2_2_g_9_44_2:j_id_3k_4_2_2_g_9_44_3_1_2_2_1_1:fieldid_8401typeSelectField1CombosCombo_input"]'
        fato_gerador_input = 'select[id="j_id_3k_1:j_id_3k_4_2_2_m_9_44_2:j_id_3k_4_2_2_m_9_44_3_1_2_2_1_1:fieldid_9239typeSelectField1CombosCombo_input"]'
        objeto_input = 'select[id="j_id_3k_1:j_id_3k_4_2_2_n_9_44_2:j_id_3k_4_2_2_n_9_44_3_1_2_2_1_1:fieldid_8405typeSelectField1CombosCombo_input"]'
        
        empresa_combo = "div[id='j_id_3k_1:comboClientProcessoParte']"
        empresa_input = "input[id='j_id_3k_1:comboClientProcessoParte_filter']"
        
        tipo_parte_contraria_input = "div[id='j_id_3k_1:j_id_3k_4_2_2_5_9_9_1:j_id_3k_4_2_2_5_9_9_4_2_m_input']"

        css_list_tipo_parte = 'div[id="j_id_3k_1:j_id_3k_4_2_2_5_9_9_1:j_id_3k_4_2_2_5_9_9_4_2_m"]'
        seach_tipo_parte_css = 'input[id="j_id_3k_1:j_id_3k_4_2_2_5_9_9_1:j_id_3k_4_2_2_5_9_9_4_2_m_filter"]'
        
        css_table_tipo_doc = 'table[id="j_id_3k_1:j_id_3k_4_2_2_5_9_9_1:tipoDocumentoInput"]'
        css_campo_doc = 'input[id="j_id_3k_1:j_id_3k_4_2_2_5_9_9_1:cpfCnpjInput"]'
        css_search_button = 'button[id="j_id_3k_1:j_id_3k_4_2_2_5_9_9_1:j_id_3k_4_2_2_5_9_9_4_2_f"]'
        
    
    classes: dict[str, Union[AME]] = {
        "AME": AME
    }
    
    def __init__(self, state: str) -> None:
        
        # Se o estado passado existir no dicionário, atualiza as variáveis
        self.state_class: Union[elements_elaw.AME] = self.classes[state]
                
    def __call__(self, *args, **kwds) -> Union[AME, Union[str, AME.condenacao, AME.custas]]:
        return self.state_class
        
    def __getattr__(self, nome_do_atributo: str) -> Callable[[], str]:
        item = getattr(self.state_class, nome_do_atributo, None)
        if not item:
            raise AttributeError(f"Atributo '{nome_do_atributo}' não encontrado na classe '{self.state_class.__name__}'")
        return item
