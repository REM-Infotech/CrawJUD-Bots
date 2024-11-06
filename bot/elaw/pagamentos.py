""" Crawler ELAW Cadastro"""

import os
import time
from time import sleep
from contextlib import suppress

from bot.CrawJUD import CrawJUD
from pytz import timezone
from bot.common.exceptions import ErroDeExecucao
from datetime import datetime

# Selenium Imports
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

type_doc = {11: "cpf", 14: "cnpj"}


class sol_pags(CrawJUD):

    interact = None

    def __getattr__(self, nome):
        return super().__getattr__(nome)

    def __init__(self, **kwrgs) -> None:
        super().__init__(**kwrgs)
        super().auth_bot()
        self.start_time = time.perf_counter()

    def execution(self) -> None:

        frame = self.dataFrame()
        self.max_rows = len(frame)

        for pos, value in enumerate(frame):

            self.row = pos + 1
            self.bot_data = self.elawFormats(value)
            if self.isStoped:
                break

            if self.driver.title.lower() == "a sessao expirou":
                self.auth(self)

            try:
                self.queue()

            except Exception as e:

                old_message = self.message
                message_error = str(e)

                self.type_log = "error"
                self.message_error = f"{message_error}. | Operação: {old_message}"
                self.prt()

                self.bot_data.update({"MOTIVO_ERRO": self.message_error})
                self.append_error(self.bot_data)

                self.message_error = None

        self.finalize_execution()

    def queue(self) -> None:

        try:
            search = self.search()

            if search is True:

                namedef = self.format_String(self.bot_data.get("TIPO_PAGAMENTO"))
                self.new_payment()
                self.set_pgto(namedef)
                pgto = getattr(self, namedef.lower())
                pgto()

                self.save_changes()
                self.append_success(self.confirm_save())

            elif search is not True:
                self.message = "Processo não encontrado!"
                self.type_log = "error"
                self.prt()
                self.append_error([self.bot_data.get("NUMERO_PROCESSO"), self.message])

        except Exception as e:
            raise ErroDeExecucao(e=e)

    def new_payment(self) -> None:

        try:
            tab_pagamentos: WebElement = self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        'a[href="#tabViewProcesso:processoValorPagamento"]',
                    )
                )
            )
            tab_pagamentos.click()

            novo_pgto: WebElement = self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        'button[id="tabViewProcesso:pvp-pgBotoesValoresPagamentoBtnNovo"]',
                    )
                )
            )
            novo_pgto.click()

        except Exception as e:
            raise ErroDeExecucao(e=e)

    def set_pgto(self, namedef: str):

        try:
            self.message = "Informando tipo de pagamento"
            self.type_log = "log"
            self.prt()

            css_typeitens = 'div[id="processoValorPagamentoEditForm:pvp:processoValorPagamentoTipoCombo"]'
            type_itens: WebElement = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_typeitens))
            )
            type_itens.click()

            sleep(0.5)

            listitens_css = 'ul[id="processoValorPagamentoEditForm:pvp:processoValorPagamentoTipoCombo_items"]'
            list_itens: WebElement = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, listitens_css))
            )
            list_itens = list_itens.find_elements(By.TAG_NAME, "li")

            for item in list_itens:

                item: WebElement = item

                normalizado_text = self.format_String(item.text)

                if normalizado_text.lower() == namedef.lower():
                    self.interact.click(item)
                    return

            raise ErroDeExecucao("Tipo de Pagamento não encontrado")

        except Exception as e:
            raise ErroDeExecucao(e=e)

    def condenacao(self) -> None:

        try:

            self.message = "Informando o valor da guia"
            self.type_log = "log"
            self.prt()

            text = self.bot_data.get("VALOR_GUIA")
            css_element = 'input[id="processoValorPagamentoEditForm:pvp:j_id_2m_1_i_1_1_9_1f_1:processoValorRateioAmountAllDt:0:j_id_2m_1_i_1_1_9_1f_2_2_q_input"]'
            element: WebElement = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, css_element))
            )

            sleep(0.5)
            element.send_keys(Keys.CONTROL, "a")
            element.send_keys(Keys.BACKSPACE)
            self.interact.send_key(element, text)
            self.driver.execute_script(
                f"document.querySelector('{css_element}').blur()"
            )

            self.interact.sleep_load('div[id="j_id_2x"]')

            type_doc_css = 'div[id="processoValorPagamentoEditForm:pvp:j_id_2m_1_i_2_1_9_g_1:eFileTipoCombo"]'
            div_type_doc: WebElement = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, type_doc_css))
            )
            div_type_doc.click()
            sleep(0.5)

            list_type_doc_css = 'ul[id="processoValorPagamentoEditForm:pvp:j_id_2m_1_i_2_1_9_g_1:eFileTipoCombo_items"]'
            list_type_doc: WebElement = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, list_type_doc_css))
            )
            list_type_doc = list_type_doc.find_elements(By.TAG_NAME, "li")

            for item in list_type_doc:

                item: WebElement = item
                if item.text.lower() == "guia de pagamento":
                    item.click()
                    break

            self.interact.sleep_load('div[id="j_id_2x"]')
            self.message = "Enviando guia"
            self.type_log = "log"
            self.prt()

            docs = [self.bot_data.get("DOC_GUIA")]
            calculo = self.bot_data.get("DOC_CALCULO", None)

            if calculo:
                calculos = [str(calculo)]

                if "," in str(calculo):
                    calculos = str(calculo).split(",")

                docs.extend(calculos)

            for doc in docs:

                doc = self.format_String(doc.upper())
                inputfilecss = 'input[id="processoValorPagamentoEditForm:pvp:j_id_2m_1_i_2_1_9_g_1:uploadGedEFile_input"]'
                insert_doc: WebElement = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, inputfilecss))
                )
                path_doc = os.path.join(self.output_dir_path, doc)
                insert_doc.send_keys(path_doc)

                self.interact.wait_fileupload()
                sleep(0.5)

            self.message = "Informando tipo de condenação"
            self.type_log = "log"
            self.prt()
            css_div_condenacao_type = 'div[id="processoValorPagamentoEditForm:pvp:j_id_2m_1_i_3_1_9_26_1_1_1:pvpEFBtypeSelectField1CombosCombo"]'
            div_condenacao_type: WebElement = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, css_div_condenacao_type))
            )
            div_condenacao_type.click()

            tipo_condenacao = str(self.bot_data.get("TIPO_CONDENACAO"))
            if "sentença" == tipo_condenacao.lower():

                sleep(0.5)
                sentenca = self.driver.find_element(
                    By.CSS_SELECTOR,
                    'li[id="processoValorPagamentoEditForm:pvp:j_id_2m_1_i_3_1_9_26_1_1_1:pvpEFBtypeSelectField1CombosCombo_3"]',
                )
                sentenca.click()

            elif "acórdão" == tipo_condenacao.lower():
                sleep(0.5)
                acordao = self.driver.find_element(
                    By.CSS_SELECTOR,
                    'li[id="processoValorPagamentoEditForm:pvp:j_id_2m_1_i_3_1_9_26_1_1_1:pvpEFBtypeSelectField1CombosCombo_1"]',
                )
                acordao.click()

            self.message = "Informando descrição do pagamento"
            self.type_log = "log"
            self.prt()

            desc_pagamento = str(self.bot_data.get("DESC_PAGAMENTO"))

            css_desc_pgto = 'textarea[id="processoValorPagamentoEditForm:pvp:processoValorPagamentoDescription"]'
            desc_pgto: WebElement = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, css_desc_pgto))
            )
            desc_pgto.click()
            if "\n" in desc_pagamento:
                desc_pagamento = desc_pagamento.replace("\n", "")

            elif "\t" in desc_pagamento:
                desc_pagamento = desc_pagamento.replace("\t", "")
            desc_pgto.send_keys(desc_pagamento)
            sleep(0.5)

            self.driver.execute_script(
                f"document.querySelector('{css_desc_pgto}').blur()"
            )

            self.message = "Informando data para pagamento"
            self.type_log = "log"
            self.prt()

            css_data_lancamento = 'input[id="processoValorPagamentoEditForm:pvp:processoValorPagamentoVencData_input"]'
            data_lancamento: WebElement = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, css_data_lancamento))
            )
            data_lancamento.click()
            data_lancamento.send_keys(self.bot_data.get("DATA_LANCAMENTO"))
            data_lancamento.send_keys(Keys.TAB)
            self.driver.execute_script(
                f"document.querySelector('{css_data_lancamento}').blur()"
            )

            self.interact.sleep_load('div[id="j_id_2x"]')
            self.message = "Informando favorecido"
            self.type_log = "log"
            self.prt()

            css_inputfavorecido = 'input[id="processoValorPagamentoEditForm:pvp:processoValorFavorecido_input"]'
            input_favorecido: WebElement = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, css_inputfavorecido))
            )
            input_favorecido.click()
            input_favorecido.clear()
            sleep(2)

            input_favorecido.send_keys(
                self.bot_data.get("CNPJ_FAVORECIDO", "00.360.305/0001-04")
            )

            result_favorecido: WebElement = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        'li[class="ui-autocomplete-item ui-autocomplete-list-item ui-corner-all ui-state-highlight"]',
                    )
                )
            )
            result_favorecido.click()

            self.interact.sleep_load('div[id="j_id_2x"]')
            self.message = "Informando forma de pagamento"
            self.type_log = "log"
            self.prt()

            label_forma_pgto = self.driver.find_element(
                By.CSS_SELECTOR,
                'div[id="processoValorPagamentoEditForm:pvp:j_id_2m_1_i_8_1_9_26_1_2_1:pvpEFSpgTypeSelectField1CombosCombo"]',
            )
            label_forma_pgto.click()

            sleep(1)
            boleto = self.driver.find_element(
                By.CSS_SELECTOR,
                'li[id="processoValorPagamentoEditForm:pvp:j_id_2m_1_i_8_1_9_26_1_2_1:pvpEFSpgTypeSelectField1CombosCombo_1"]',
            )
            boleto.click()

            self.interact.sleep_load('div[id="j_id_2x"]')

            css_cod_bars = 'input[id="processoValorPagamentoEditForm:pvp:j_id_2m_1_i_8_1_9_26_1_2_1:j_id_2m_1_i_8_1_9_26_1_2_c_2:j_id_2m_1_i_8_1_9_26_1_2_c_5:0:j_id_2m_1_i_8_1_9_26_1_2_c_15:j_id_2m_1_i_8_1_9_26_1_2_c_1v"]'
            campo_cod_barras: WebElement = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, css_cod_bars))
            )
            campo_cod_barras.click()
            sleep(0.5)

            cod_barras = str(self.bot_data.get("COD_BARRAS"))
            campo_cod_barras.send_keys(cod_barras.replace("\t", "").replace("\n", ""))
            self.driver.execute_script(
                f"document.querySelector('{css_cod_bars}').blur()"
            )

            self.interact.sleep_load('div[id="j_id_2x"]')
            self.message = "Informando centro de custas"
            self.type_log = "log"
            self.prt()

            css_centro_custas = 'input[id="processoValorPagamentoEditForm:pvp:j_id_2m_1_i_9_1_9_26_1_1_1:pvpEFBfieldText"]'
            centro_custas: WebElement = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, css_centro_custas))
            )
            centro_custas.click()
            centro_custas.send_keys("A906030100")

            self.driver.execute_script(
                f"document.querySelector('{css_centro_custas}').blur()"
            )

            sleep(1)
            self.message = "Informando conta para débito"
            self.type_log = "log"
            self.prt()

            css_div_conta_debito = 'div[id="processoValorPagamentoEditForm:pvp:j_id_2m_1_i_a_1_9_26_1_1_1:pvpEFBtypeSelectField1CombosCombo"]'
            div_conta_debito: WebElement = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, css_div_conta_debito))
            )
            div_conta_debito.click()
            sleep(1)
            conta_debito = self.driver.find_element(
                By.CSS_SELECTOR,
                'li[data-label="AMAZONAS - PAGTO CONDENAÇÕES DE LITÍGIOS CÍVEIS CONTRAPARTIDA"]',
            )
            conta_debito.click()

        except Exception as e:
            raise ErroDeExecucao(e=e)

    def custas(self) -> None:

        try:

            self.message = "Informando valor da guia"
            self.type_log = "log"
            self.prt()

            valor_doc = self.bot_data.get("VALOR_GUIA").replace(".", ",")
            valor_guia = (
                'input[id="processoValorPagamentoEditForm:pvp:valorField_input"]'
            )
            element: WebElement = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, valor_guia))
            )
            element.click()
            element.send_keys(Keys.CONTROL, "a")
            sleep(0.5)
            element.send_keys(Keys.BACK_SPACE)
            sleep(0.5)
            element.send_keys(valor_doc)

            css_Valor_guia = (
                'input[id="processoValorPagamentoEditForm:pvp:valorField_input"]'
            )
            self.driver.execute_script(
                f"document.querySelector('{css_Valor_guia}').blur()"
            )

            sleep(0.5)

            css_tipo_doc = 'div[id="processoValorPagamentoEditForm:pvp:j_id_2m_1_i_2_1_9_g_1:eFileTipoCombo"]'
            list_tipo_doc: WebElement = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_tipo_doc))
            )
            list_tipo_doc.click()
            sleep(1)

            css_gru = 'li[id="processoValorPagamentoEditForm:pvp:j_id_2m_1_i_2_1_9_g_1:eFileTipoCombo_35"]'
            set_gru = self.driver.find_element(By.CSS_SELECTOR, css_gru)
            set_gru.click()

            sleep(2)
            self.message = "Inserindo documento"
            self.type_log = "log"
            self.prt()

            docs = [self.bot_data.get("DOC_GUIA")]

            for doc in docs:

                doc = self.format_String(doc)
                insert_doc: WebElement = self.wait.until(
                    EC.presence_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            'input[id="processoValorPagamentoEditForm:pvp:j_id_2m_1_i_2_1_9_g_1:uploadGedEFile_input"]',
                        )
                    )
                )
                insert_doc.send_keys(f"{self.output_dir_path}/{doc}")

                wait_upload: WebElement = (
                    WebDriverWait(self.driver, 20)
                    .until(
                        EC.presence_of_element_located(
                            (
                                By.CSS_SELECTOR,
                                'div[id="processoValorPagamentoEditForm:pvp:j_id_2m_1_i_2_1_9_g_1:gedEFileDataTable"]',
                            )
                        )
                    )
                    .find_element(By.TAG_NAME, "table")
                    .find_element(By.TAG_NAME, "tbody")
                    .find_elements(By.TAG_NAME, "tr")
                )

                if len(wait_upload) == len(docs):
                    break

            solicitante = str(self.bot_data.get("SOLICITANTE")).lower()
            if "monitoria" == solicitante or "monitória" == solicitante.lower():
                desc_pgto_css = 'textarea[id="processoValorPagamentoEditForm:pvp:processoValorPagamentoDescription"]'
                desc_pgto: WebElement = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, desc_pgto_css))
                )
                desc_pgto.send_keys(self.bot_data.get("DESC_PAGAMENTO"))
                self.driver.execute_script(
                    f"document.querySelector('{desc_pgto_css}').blur()"
                )

            self.message = "Informando tipo de guia"
            self.type_log = "log"
            self.prt()

            css_tipocusta = 'div[id="processoValorPagamentoEditForm:pvp:j_id_2m_1_i_4_1_9_26_1_1_1:pvpEFBtypeSelectField1CombosCombo"]'
            div_tipo_custa = self.driver.find_element(By.CSS_SELECTOR, css_tipocusta)
            div_tipo_custa.click()
            sleep(1)

            tipo_guia = str(self.bot_data.get("TIPO_GUIA"))
            css_listcusta = 'ul[id="processoValorPagamentoEditForm:pvp:j_id_2m_1_i_4_1_9_26_1_1_1:pvpEFBtypeSelectField1CombosCombo_items"]'
            list_tipo_custa: WebElement = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_listcusta))
            )
            list_tipo_custa = list_tipo_custa.find_elements(By.TAG_NAME, "li")
            for item in list_tipo_custa:

                item: WebElement = item
                if tipo_guia.lower() == item.text.lower():

                    sleep(0.5)
                    item.click()
                    break

            sleep(1)
            self.message = "Informando data para pagamento"
            self.type_log = "log"
            self.prt()

            css_data_vencimento = 'input[id="processoValorPagamentoEditForm:pvp:processoValorPagamentoVencData_input"]'
            data_vencimento = self.driver.find_element(
                By.CSS_SELECTOR, css_data_vencimento
            )
            data_vencimento.click()
            data_vencimento.send_keys(self.bot_data.get("DATA_LANCAMENTO"))
            self.driver.execute_script(
                f"document.querySelector('{css_data_vencimento}').blur()"
            )
            self.interact.sleep_load('div[id="j_id_2x"]')

            css_formapgto = 'div[id="processoValorPagamentoEditForm:pvp:j_id_2m_1_i_8_1_9_26_1_2_1:pvpEFSpgTypeSelectField1CombosCombo"]'
            label_forma_pgto = self.driver.find_element(By.CSS_SELECTOR, css_formapgto)
            label_forma_pgto.click()

            sleep(1)
            css_boleto = 'li[id="processoValorPagamentoEditForm:pvp:j_id_2m_1_i_8_1_9_26_1_2_1:pvpEFSpgTypeSelectField1CombosCombo_1"]'
            boleto = self.driver.find_element(By.CSS_SELECTOR, css_boleto)
            boleto.click()

            self.interact.sleep_load('div[id="j_id_2x"]')

            css_campo_cod_barras = 'input[id="processoValorPagamentoEditForm:pvp:j_id_2m_1_i_8_1_9_26_1_2_1:j_id_2m_1_i_8_1_9_26_1_2_c_2:j_id_2m_1_i_8_1_9_26_1_2_c_5:0:j_id_2m_1_i_8_1_9_26_1_2_c_15:j_id_2m_1_i_8_1_9_26_1_2_c_1v"]'
            campo_cod_barras: WebElement = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_campo_cod_barras))
            )
            campo_cod_barras.click()
            sleep(0.5)
            campo_cod_barras.send_keys(self.bot_data.get("COD_BARRAS"))
            self.driver.execute_script(
                f"document.querySelector('{css_campo_cod_barras}').blur()"
            )

            self.message = "Informando favorecido"
            self.type_log = "log"
            self.prt()

            sleep(2)
            input_favorecido: WebElement = self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        'input[id="processoValorPagamentoEditForm:pvp:processoValorFavorecido_input"]',
                    )
                )
            )
            input_favorecido.click()
            sleep(1)
            input_favorecido.clear()

            input_favorecido.send_keys(
                self.bot_data.get("CNPJ_FAVORECIDO", "04.812.509/0001-90")
            )

            result_favorecido: WebElement = self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        'li[class="ui-autocomplete-item ui-autocomplete-list-item ui-corner-all ui-state-highlight"]',
                    )
                )
            )
            result_favorecido.click()
            css_input_favorecido = 'input[id="processoValorPagamentoEditForm:pvp:processoValorFavorecido_input"]'
            self.driver.execute_script(
                f"document.querySelector('{css_input_favorecido}').blur()"
            )

            self.message = "Informando centro de custas"
            self.type_log = "log"
            self.prt()

            sleep(1)

            css_centro_custas = 'input[id="processoValorPagamentoEditForm:pvp:j_id_2m_1_i_9_1_9_26_1_1_1:pvpEFBfieldText"]'
            centro_custas: WebElement = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_centro_custas))
            )
            centro_custas.click()
            centro_custas.send_keys("A906030100")

            self.driver.execute_script(
                f"document.querySelector('{css_centro_custas}').blur()"
            )

            sleep(1)

            css_conta_debito = 'div[id="processoValorPagamentoEditForm:pvp:j_id_2m_1_i_a_1_9_26_1_1_1:pvpEFBtypeSelectField1CombosCombo"]'
            div_conta_debito: WebElement = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_conta_debito))
            )
            div_conta_debito.click()
            sleep(1)

            if "jec" == solicitante:
                conta_debito = self.driver.find_element(
                    By.CSS_SELECTOR, 'li[data-label="CUSTAS JUDICIAIS CIVEIS"]'
                )
                conta_debito.click()

            elif "monitoria" == solicitante or "monitória" == solicitante:
                conta_debito = self.driver.find_element(
                    By.CSS_SELECTOR, 'li[data-label="CUSTAS JUDICIAIS - MONITORIAS"]'
                )
                conta_debito.click()

        except Exception as e:
            raise ErroDeExecucao(e=e)

    def save_changes(self) -> None:

        try:

            self.message = "Salvando alterações"
            self.type_log = "log"
            self.prt()
            save: WebElement = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        'button[id="processoValorPagamentoEditForm:btnSalvarProcessoValorPagamento"]',
                    )
                )
            )
            save.click()

        except Exception as e:
            raise ErroDeExecucao(e=e)

    def confirm_save(self) -> None:

        try:
            tab_pagamentos: WebElement = self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        'a[href="#tabViewProcesso:processoValorPagamento"]',
                    )
                )
            )
            tab_pagamentos.click()

            enter_table: WebElement = (
                self.wait.until(
                    EC.presence_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            'div[id="tabViewProcesso:pvp-dtProcessoValorResults"]',
                        )
                    )
                )
                .find_element(By.TAG_NAME, "table")
                .find_element(By.TAG_NAME, "tbody")
            )
            check_solicitacoes = enter_table.find_elements(By.TAG_NAME, "tr")
            info_sucesso = [
                self.bot_data.get("NUMERO_PROCESSO"),
                "Pagamento solicitado com sucesso!!",
            ]
            current_handle = self.driver.current_window_handle

            for pos, item in enumerate(check_solicitacoes):

                if item.text == "Nenhum registro encontrado!":
                    raise ErroDeExecucao("Pagamento não solicitado")

                open_details = item.find_element(By.CSS_SELECTOR, 'button[title="Ver"]')
                open_details.click()

                sleep(1)
                id_task = item.find_elements(By.TAG_NAME, "td")[2].text
                closeContext = self.wait.until(
                    EC.presence_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            f'div[id="tabViewProcesso:pvp-dtProcessoValorResults:{pos}:pvp-pgBotoesValoresPagamentoBtnVer_dlg"]'
                        )
                    )
                ).find_element(By.TAG_NAME, "a")

                WaitFrame = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'iframe[title="Valor"]')
                    )
                )
                self.driver.switch_to.frame(WaitFrame)

                tipoCusta = ""
                cod_bars = ""
                tipoCondenacao = ""
                now = datetime.now(timezone("America/Manaus")).strftime(
                    "%d-%m-%Y %H.%M.%S"
                )
                Name_Comprovante1 = f"COMPROVANTE 1 {self.bot_data.get("NUMERO_PROCESSO")} - {self.pid} - {now}.png"
                cod_bars_xls = str(
                    self.bot_data.get("COD_BARRAS").replace(".", "").replace(" ", "")
                )

                with suppress(TimeoutException):
                    tipoCusta = str(
                        self.wait.until(
                            EC.presence_of_element_located(
                                (
                                    By.CSS_SELECTOR,
                                    r"#processoValorPagamentoView\:j_id_p_1_2_1_2_1 > table > tbody > tr:nth-child(5)",
                                )
                            )
                        )
                        .text.split(":")[-1]
                        .replace("\n", "")
                    )

                with suppress(TimeoutException):
                    cod_bars = str(
                        self.wait.until(
                            EC.presence_of_element_located(
                                (
                                    By.CSS_SELECTOR,
                                    r"#processoValorPagamentoView\:j_id_p_1_2_1_2_7_8_4_23_1\:j_id_p_1_2_1_2_7_8_4_23_2_1_2_1\:j_id_p_1_2_1_2_7_8_4_23_2_1_2_2_1_3 > table > tbody > tr:nth-child(3)",
                                )
                            )
                        )
                        .text.split(":")[-1]
                        .replace("\n", "")
                    )

                with suppress(TimeoutException):
                    tipoCondenacao = (
                        self.wait.until(
                            EC.presence_of_element_located(
                                (
                                    By.CSS_SELECTOR,
                                    r"#processoValorPagamentoView\:j_id_p_1_2_1_2_1 > table > tbody > tr:nth-child(4)",
                                )
                            )
                        )
                        .text.split(":")[-1]
                        .replace("\n", "")
                    )

                namedef = self.format_String(
                    self.bot_data.get("TIPO_PAGAMENTO")
                ).lower()

                chk_bars = cod_bars == cod_bars_xls

                if namedef == "condenacao":
                    tipo_condenacao_xls = str(self.bot_data.get("TIPO_CONDENACAO", ""))
                    match_condenacao = (
                        tipo_condenacao_xls.lower() == tipoCondenacao.lower()
                    )
                    matchs = all([match_condenacao, chk_bars])

                elif namedef == "custas":
                    tipo_custa_xls = str(self.bot_data.get("TIPO_GUIA", ""))
                    match_custa = tipo_custa_xls.lower() == tipoCusta.lower()
                    matchs = all([match_custa, chk_bars])

                if matchs:
                    self.driver.switch_to.default_content()
                    url_page = WaitFrame.get_attribute("src")
                    self.getScreenShot(url_page, Name_Comprovante1)
                    self.driver.switch_to.window(current_handle)

                    closeContext.click()
                    Name_Comprovante2 = f"COMPROVANTE 2 {self.bot_data.get("NUMERO_PROCESSO")} - {self.pid} - {now}.png"
                    item.screenshot(
                        os.path.join(self.output_dir_path, Name_Comprovante2)
                    )

                    info_sucesso.extend(
                        [
                            tipoCondenacao,
                            Name_Comprovante1,
                            id_task,
                            Name_Comprovante2,
                        ]
                    )
                    return info_sucesso

                self.driver.switch_to.default_content()
                closeContext.click()
                sleep(0.25)

            raise ErroDeExecucao("Pagamento não solicitado")

        except Exception as e:
            raise ErroDeExecucao(e=e)

    def getScreenShot(self, url_page: str, Name_Comprovante1: str):

        self.driver.switch_to.new_window("tab")
        self.driver.get(url_page)
        self.driver.save_screenshot(
            os.path.join(self.output_dir_path, Name_Comprovante1)
        )
        self.driver.close()
