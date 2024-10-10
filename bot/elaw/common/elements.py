from typing import Union, Any
class elements_elaw:
    
    class AME:
        
        class condenacao:
            string = ""
            
        class custas:
            
            string = ""
        
        numero_processo = "input[id='j_id_3k_1:j_id_3k_4_2_2_2_9_f_2:txtNumeroMask']"
        
        estado_combo = "div[id='j_id_3k_1:j_id_3k_4_2_2_1_9_u_1:comboEstadoVara']"
        estado_panel = "div[id='j_id_3k_1:j_id_3k_4_2_2_1_9_u_1:comboEstadoVara_panel']"
        
        comarca_combo = "div[id='j_id_3k_1:j_id_3k_4_2_2_1_9_u_1:comboComarcaVara']"
        comarca_panel = "div[id='j_id_3k_1:j_id_3k_4_2_2_1_9_u_1:comboComarcaVara_panel']"

        foro_combo = "div[id='j_id_3k_1:j_id_3k_4_2_2_1_9_u_1:comboForoTribunal']"
        foro_panel = "div[id='j_id_3k_1:j_id_3k_4_2_2_1_9_u_1:comboForoTribunal_panel']"
        vara_combo = "div[id='j_id_3k_1:j_id_3k_4_2_2_1_9_u_1:comboVara']"
        vara_panel = "div[id='j_id_3k_1:j_id_3k_4_2_2_1_9_u_1:comboVara_panel']"
        
        empresa_combo = "div[id='j_id_3k_1:comboClientProcessoParte']"
        empresa_panel = "input[id='j_id_3k_1:comboClientProcessoParte_filter']"
        
        tipo_empresa_combo = "div[id='j_id_3k_1:j_id_3k_4_2_2_4_9_2_5']"
        tipo_empresa_panel = "div[id='j_id_3k_1:j_id_3k_4_2_2_4_9_2_5_panel']"
        
        tipo_parte_contraria_combo = "div[id='j_id_3k_1:j_id_3k_4_2_2_5_9_9_1:j_id_3k_4_2_2_5_9_9_4_2_m']"
        tipo_parte_contraria_panel = "div[id='j_id_3k_1:j_id_3k_4_2_2_5_9_9_1:j_id_3k_4_2_2_5_9_9_4_2_m_panel']"

        ##
        css_list_tipo_parte = 'div[id="j_id_3k_1:j_id_3k_4_2_2_5_9_9_1:j_id_3k_4_2_2_5_9_9_4_2_m"]'
        seach_tipo_parte_css = 'input[id="j_id_3k_1:j_id_3k_4_2_2_5_9_9_1:j_id_3k_4_2_2_5_9_9_4_2_m_filter"]'
        
        css_table_tipo_doc = 'table[id="j_id_3k_1:j_id_3k_4_2_2_5_9_9_1:tipoDocumentoInput"]'
        css_campo_doc = 'input[id="j_id_3k_1:j_id_3k_4_2_2_5_9_9_1:cpfCnpjInput"]'
        css_search_button = 'button[id="j_id_3k_1:j_id_3k_4_2_2_5_9_9_1:j_id_3k_4_2_2_5_9_9_4_2_f"]'
        
        ##
        url_login = ""
        campo_username = ''
        campo_passwd = ''
        btn_entrar = ''
        chk_login = ''
        
        url_busca = ""
        btn_busca = ""
    
    classes: dict[str, Union[AME]] = {
        "AME": AME
    }    
    
    def __init__(self, state: str) -> None:
        
        # Se o estado passado existir no dicionário, atualiza as variáveis
        self.state_class: Union[elements_elaw.AME] = self.classes[state]
                
    def __call__(self, *args, **kwds) -> Union[AME, Union[str, AME.condenacao, AME.custas]]:
        return self.state_class
        
    def __getattr__(self, nome_do_atributo: str) -> Any:
        item = getattr(self.state_class, nome_do_atributo, None)
        if not item:
            raise AttributeError(f"Atributo '{nome_do_atributo}' não encontrado na classe '{self.state_class.__name__}'")
        return item
