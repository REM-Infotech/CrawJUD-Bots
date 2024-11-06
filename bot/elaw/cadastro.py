""" Crawler ELAW Cadastro"""

import os
import time
from time import sleep
from contextlib import suppress
from bot.CrawJUD import CrawJUD
from bot.common.exceptions import ErroDeExecucao
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

# Selenium Imports


type_doc = {11: "cpf", 14: "cnpj"}


class cadastro(CrawJUD):

    def __init__(self, **kwrgs) -> None:
        super().__init__(**kwrgs)
        super().auth_bot()
        self.start_time = time.perf_counter()

    def execution(self) -> None:

        frame = self.dataFrame()
        self.max_rows = len(frame)

        for pos, value in enumerate(frame):

            self.row = pos + 1
            self.bot_data = value
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

        self.bot_data = self.elawFormats(self.bot_data)
        search = self.search()

        if search is True:

            self.append_success(
                [
                    self.bot_data.get("NUMERO_PROCESSO"),
                    "Processo já cadastrado!",
                    self.pid,
                ]
            )

        elif search is not True:

            self.message = "Processo não encontrado, inicializando cadastro..."
            self.type_log = "log"
            self.prt()

            btn_newproc = self.driver.find_element(
                By.CSS_SELECTOR, 'button[id="btnNovo"]'
            )
            btn_newproc.click()

            start_time = time.perf_counter()

            self.area_direito()
            self.subarea_direito()
            self.next_page()
            self.info_localizacao()
            self.informa_estado()
            self.informa_comarca()
            self.informa_foro()
            self.informa_vara()
            self.informa_proceso()
            self.informa_empresa()
            self.set_classe_empresa()
            self.parte_contraria()
            self.uf_proc()
            self.acao_proc()
            self.advogado_responsavel()
            self.adv_parte_contraria()
            self.data_distribuicao()
            self.info_valor_causa()
            self.escritorio_externo()
            self.tipo_contingencia()

            end_time = time.perf_counter()
            execution_time = end_time - start_time
            calc = execution_time / 60
            splitcalc = str(calc).split(".")
            minutes = int(splitcalc[0])
            seconds = int(float(f"0.{splitcalc[1]}") * 60)

            self.message = (
                f"Formulário preenchido em {minutes} minutos e {seconds} segundos"
            )
            self.type_log = "log"
            self.prt()

            self.salvar_tudo()

            if self.confirm_save() is True:
                self.print_comprovante()

    def area_direito(self) -> None:
        """Declaração dos CSS em variáveis"""
        css_label_area = 'div[id="comboArea"]'
        elemento = 'div[id="comboArea_panel"]'

        self.message = "Informando área do direito"
        self.type_log = "log"
        self.prt()

        label_area: WebElement = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_label_area)),
            message="Erro ao encontrar elemento",
        )
        label_area.click()
        text = str(self.bot_data.get("AREA_DIREITO"))
        sleep(0.5)

        self.interact.select_item(elemento, text)
        self.interact.sleep_load('div[id="j_id_3w"]')

        self.message = "Área do direito selecionada!"
        self.type_log = "info"
        self.prt()

    def subarea_direito(self) -> None:
        """Declaração dos CSS em variáveis"""
        comboAreaSub_css = 'div[id="comboAreaSub"]'
        elemento = 'div[id="comboAreaSub_panel"]'

        self.message = "Informando sub-área do direito"
        self.type_log = "log"
        self.prt()

        expand_areasub: WebElement = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, comboAreaSub_css)),
            message="Erro ao encontrar elemento",
        )
        expand_areasub.click()
        text = str(self.bot_data.get("SUBAREA_DIREITO"))
        sleep(0.5)

        self.interact.select_item(elemento, text)
        self.interact.sleep_load('div[id="j_id_3x"]')
        self.message = "Sub-Área do direito selecionada!"
        self.type_log = "info"
        self.prt()

    def next_page(self) -> None:

        css_button = 'button[id="btnContinuar"]'
        next_page: WebElement = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_button)),
            message="Erro ao encontrar elemento",
        )
        next_page.click()

    def info_localizacao(self) -> None:

        css_esfera_judge = 'div[id="j_id_3k_1:j_id_3k_4_2_2_1_9_u_1:comboRito"]'
        elemento = 'div[id="j_id_3k_1:j_id_3k_4_2_2_1_9_u_1:comboRito_panel"]'

        self.message = "Informando esfera do processo"
        self.type_log = "log"
        self.prt()

        set_esfera_judge: WebElement = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_esfera_judge)),
            message="Erro ao encontrar elemento",
        )
        set_esfera_judge.click()
        sleep(0.5)

        self.interact.select_item(elemento, "Judicial")
        self.interact.sleep_load('div[id="j_id_3x"]')

        self.message = "Esfera Informada!"
        self.type_log = "info"
        self.prt()

    def informa_estado(self) -> None:
        """Declaração dos CSS em variáveis"""

        key = "ESTADO"
        elementSelect = self.elements.estado_input
        text = str(self.bot_data.get(key, None))

        self.message = "Informando estado do processo"
        self.type_log = "log"
        self.prt()

        self.Select2_ELAW(elementSelect, text)
        self.interact.sleep_load('div[id="j_id_3x"]')

        self.message = "Estado do processo informado!"
        self.type_log = "log"
        self.prt()

    def informa_comarca(self) -> None:
        """Declaração dos CSS em variáveis"""

        text = str(self.bot_data.get("COMARCA"))
        elementSelect = self.elements.comarca_input

        self.message = "Informando comarca do processo"
        self.type_log = "log"
        self.prt()

        self.Select2_ELAW(elementSelect, text)
        self.interact.sleep_load('div[id="j_id_3x"]')

        self.message = "Comarca do processo informado!"
        self.type_log = "log"
        self.prt()

    def informa_foro(self) -> None:
        """Declaração dos CSS em variáveis"""

        elementSelect = self.elements.foro_input
        text = str(self.bot_data.get("FORO"))

        self.message = "Informando foro do processo"
        self.type_log = "log"
        self.prt()

        self.Select2_ELAW(elementSelect, text)
        self.interact.sleep_load('div[id="j_id_3x"]')

        self.message = "Foro do processo informado!"
        self.type_log = "log"
        self.prt()

    def informa_vara(self) -> None:
        """Declaração dos CSS em variáveis"""

        text = self.bot_data.get("VARA")
        elementSelect = self.elements.vara_input

        self.message = "Informando vara do processo"
        self.type_log = "log"
        self.prt()

        self.Select2_ELAW(elementSelect, text)
        self.interact.sleep_load('div[id="j_id_3x"]')

        self.message = "Vara do processo informado!"
        self.type_log = "log"
        self.prt()

    def informa_proceso(self) -> None:

        key = "NUMERO_PROCESSO"
        css_campo_processo = self.elements.numero_processo

        self.message = "Informando número do processo"
        self.type_log = "log"
        self.prt()

        campo_processo: WebElement = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_campo_processo)),
            message="Erro ao encontrar elemento",
        )
        campo_processo.click()

        self.interact.send_key(campo_processo, self.bot_data.get(key))

        self.driver.execute_script(
            f'document.querySelector("{css_campo_processo}").blur()'
        )
        self.interact.sleep_load('div[id="j_id_3x"]')

        self.message = "Número do processo informado!"
        self.type_log = "info"
        self.prt()

    def informa_empresa(self) -> None:

        text = self.bot_data.get("EMPRESA")
        elementSelect = self.elements.empresa_input

        self.message = "Informando Empresa"
        self.type_log = "log"
        self.prt()

        self.Select2_ELAW(elementSelect, text)
        self.interact.sleep_load('div[id="j_id_3x"]')

        self.message = "Empresa informada!"
        self.type_log = "info"
        self.prt()

    def set_classe_empresa(self) -> None:
        """Declaração dos CSS em variáveis"""

        key = "TIPO_EMPRESA"
        elementSelect = self.elements.tipo_empresa_input
        text = self.bot_data.get(key).__str__().capitalize()

        self.message = "Informando classificação da Empresa"
        self.type_log = "log"
        self.prt()

        self.Select2_ELAW(elementSelect, text)
        self.interact.sleep_load('div[id="j_id_3x"]')

        self.message = "Classificação da Empresa informada"
        self.type_log = "info"
        self.prt()

    def parte_contraria(self) -> None:

        self.message = "Preechendo informações da parte contrária"
        self.type_log = "log"
        self.prt()

        text = self.bot_data.get("TIPO_PARTE_CONTRARIA")
        elementSelect = self.elements.tipo_parte_contraria_input
        self.Select2_ELAW(elementSelect, text)

        table_tipo_doc: WebElement = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, self.elements.css_table_tipo_doc)
            ),
            message="Erro ao encontrar elemento",
        )
        table_tipo_doc = table_tipo_doc.find_elements(By.TAG_NAME, "td")
        self.interact.sleep_load('div[id="j_id_3x"]')

        for item in table_tipo_doc:
            item: WebElement = item
            get_label = str(item.find_element(By.TAG_NAME, "label").text).lower()
            tipo_doc = type_doc.get(
                len(
                    "".join(
                        filter(str.isdigit, self.bot_data.get("DOC_PARTE_CONTRARIA"))
                    )
                )
            )

            if get_label == tipo_doc:

                select_button = item.find_element(
                    By.CSS_SELECTOR, 'div[class="ui-radiobutton ui-widget"]'
                )
                select_button.click()
                break

        self.interact.sleep_load('div[id="j_id_3x"]')
        campo_doc: WebElement = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, self.elements.css_campo_doc)
            ),
            message="Erro ao encontrar elemento",
        )
        campo_doc.click()
        sleep(0.05)
        campo_doc.clear()
        sleep(0.05)
        self.interact.send_key(campo_doc, self.bot_data.get("DOC_PARTE_CONTRARIA"))
        self.interact.sleep_load('div[id="j_id_3x"]')

        search_button_parte: WebElement = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, self.elements.css_search_button)
            ),
            message="Erro ao encontrar elemento",
        )
        search_button_parte.click()
        self.interact.sleep_load('div[id="j_id_3x"]')

        check_parte = self.check_part_found(self.driver)

        if not check_parte:
            try:
                self.cad_parte()
                self.driver.switch_to.default_content()
                self.interact.sleep_load('div[id="j_id_3x"]')

            except Exception as e:
                raise ErroDeExecucao("Não foi possível cadastrar parte", e)

        self.messsage = "Parte adicionada!"
        self.type_log = "info"
        self.prt()

    def uf_proc(self) -> None:

        css_div_select_opt = 'div[id="j_id_3k_1:j_id_3k_4_2_2_9_9_44_2:j_id_3k_4_2_2_9_9_44_3_1_2_2_2_1:fieldid_9240pgTypeSelectField1CombosCombo"]'
        elemento = 'div[id="j_id_3k_1:j_id_3k_4_2_2_9_9_44_2:j_id_3k_4_2_2_9_9_44_3_1_2_2_2_1:fieldid_9240pgTypeSelectField1CombosCombo_panel"]'
        css_other_location = 'input[id="j_id_3k_1:j_id_3k_4_2_2_9_9_44_2:j_id_3k_4_2_2_9_9_44_3_1_2_2_2_1:j_id_3k_4_2_2_9_9_44_3_1_2_2_2_2_1_c:j_id_3k_4_2_2_9_9_44_3_1_2_2_2_2_1_f:0:j_id_3k_4_2_2_9_9_44_3_1_2_2_2_2_1_1f:fieldText"]'

        get_div_select_locale: WebElement = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_div_select_opt)),
            message="Erro ao encontrar elemento",
        )
        get_div_select_locale.click()
        sleep(0.5)

        text = str(self.bot_data.get("CAPITAL_INTERIOR"))
        self.interact.select_item(elemento, text)
        self.interact.sleep_load('div[id="j_id_3x"]')

        if str(self.bot_data.get("CAPITAL_INTERIOR")).lower() == "outro estado":

            other_location: WebElement = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_other_location)),
                message="Erro ao encontrar elemento",
            )
            other_location.click()
            self.interact.send_key(other_location, self.bot_data.get("ESTADO"))
            self.interact.send_key(other_location, Keys.ENTER)

    def acao_proc(self) -> None:
        """Declaração dos CSS em variáveis"""
        comboProcessoTipo = 'div[id="j_id_3k_1:comboProcessoTipo"]'
        elemento = 'input[id="j_id_3k_1:comboProcessoTipo_filter"]'

        self.message = "Informando ação do processo"
        self.type_log = "log"
        self.prt()

        div_comboProcessoTipo: WebElement = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, comboProcessoTipo)),
            message="Erro ao encontrar elemento",
        )
        div_comboProcessoTipo.click()

        elemento = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, elemento)),
            message="Erro ao encontrar elemento",
        )

        text = self.bot_data.get("ACAO")
        self.interact.click(elemento)
        self.interact.send_key(elemento, text)
        self.interact.send_key(elemento, Keys.ENTER)
        self.interact.sleep_load('div[id="j_id_3x"]')

        self.message = "Ação informada!"
        self.type_log = "info"
        self.prt()

    def data_distribuicao(self) -> None:

        self.interact.sleep_load('div[id="j_id_3x"]')
        self.message = "Informando data de distribuição"
        self.type_log = "log"
        self.prt()

        self.interact.sleep_load('div[id="j_id_3x"]')
        css_data_distribuicao = 'input[id="j_id_3k_1:dataDistribuicao_input"]'
        data_distribuicao: WebElement = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, css_data_distribuicao)),
            message="Erro ao encontrar elemento",
        )

        self.interact.clear(data_distribuicao)

        self.interact.send_key(
            data_distribuicao, self.bot_data.get("DATA_DISTRIBUICAO")
        )
        self.interact.send_key(data_distribuicao, Keys.TAB)
        self.interact.sleep_load('div[id="j_id_3x"]')

        self.message = "Data de distribuição informada!"
        self.type_log = "info"
        self.prt()

    def advogado_responsavel(self) -> None:

        self.message = "informando advogado interno"
        self.type_log = "log"
        self.prt()
        css_adv_responsavel = 'input[id="j_id_3k_1:autoCompleteLawyer_input"]'

        input_adv_responsavel: WebElement = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_adv_responsavel))
        )
        input_adv_responsavel.click()
        self.interact.send_key(
            input_adv_responsavel, self.bot_data.get("ADVOGADO_INTERNO")
        )

        css_wait_adv = r"#j_id_3k_1\:autoCompleteLawyer_panel > ul > li"

        wait_adv = None

        with suppress(TimeoutException):
            wait_adv: WebElement = WebDriverWait(self.driver, 25).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_wait_adv))
            )

        if wait_adv:
            wait_adv.click()
        elif not wait_adv:
            raise ErroDeExecucao(message="Advogado interno não encontrado")

        self.interact.sleep_load('div[id="j_id_3x"]')

        css_div_select_Adv = 'div[id="j_id_3k_1:comboAdvogadoResponsavelProcesso"]'
        div_select_Adv: WebElement = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_div_select_Adv))
        )
        div_select_Adv.click()

        self.interact.sleep_load('div[id="j_id_3x"]')

        css_input_select_Adv = (
            'input[id="j_id_3k_1:comboAdvogadoResponsavelProcesso_filter"]'
        )
        input_select_adv: WebElement = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_input_select_Adv))
        )
        input_select_adv.click()

        self.interact.send_key(input_select_adv, self.bot_data.get("ADVOGADO_INTERNO"))
        input_select_adv.send_keys(Keys.ENTER)

        self.driver.execute_script(
            f"document.querySelector('{css_div_select_Adv}').blur()"
        )

        self.interact.sleep_load('div[id="j_id_3x"]')

        self.message = "Advogado interno informado!"
        self.type_log = "info"
        self.prt()

    def adv_parte_contraria(self) -> None:

        self.message = "Informando Adv. Parte contrária"
        self.type_log = "log"
        self.prt()

        css_input_adv = 'input[id="j_id_3k_1:autoCompleteLawyerOutraParte_input"]'
        campo_adv: WebElement = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_input_adv)),
            message="Erro ao encontrar elemento",
        )
        campo_adv.click()
        campo_adv.clear()
        sleep(0.02)

        Text = str(self.bot_data.get("ADV_PARTE_CONTRARIA"))

        for i in ["\t", "\n"]:
            if i in Text:
                Text = Text.split(i)[0]
                break

        self.interact.send_key(campo_adv, Text)

        css_check_adv = r"#j_id_3k_1\:autoCompleteLawyerOutraParte_panel > ul > li.ui-autocomplete-item.ui-autocomplete-list-item.ui-corner-all.ui-state-highlight"
        check_adv = None

        self.interact.sleep_load('div[id="j_id_3x"]')

        with suppress(TimeoutException):
            check_adv: WebElement = (
                WebDriverWait(self.driver, 15)
                .until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, css_check_adv)),
                    message="Erro ao encontrar elemento",
                )
                .text
            )
            self.interact.send_key(campo_adv, Keys.ENTER)
            self.driver.execute_script(
                f"document.querySelector('{css_input_adv}').blur()"
            )

        if not check_adv:
            self.cad_adv()
            self.driver.switch_to.default_content()

        self.interact.sleep_load('div[id="j_id_3x"]')

        self.message = "Adv. parte contrária informado!"
        self.type_log = "info"
        self.prt()

    def info_valor_causa(self) -> None:

        self.message = "Informando valor da causa"
        self.type_log = "log"
        self.prt()

        css_valor_causa = 'input[id="j_id_3k_1:amountCase_input"]'

        valor_causa: WebElement = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, css_valor_causa)),
            message="Erro ao encontrar elemento",
        )

        valor_causa.click()
        sleep(0.5)
        valor_causa.clear()

        self.interact.send_key(valor_causa, self.bot_data.get("VALOR_CAUSA"))
        self.driver.execute_script(
            f"document.querySelector('{css_valor_causa}').blur()"
        )

        self.interact.sleep_load('div[id="j_id_3x"]')

        self.message = "Valor da causa informado!"
        self.type_log = "info"
        self.prt()

    def escritorio_externo(self) -> None:
        """Declaração dos CSS em variáveis"""
        escritrorioexterno = 'div[id="j_id_3k_1:comboEscritorio"]'
        elemento = 'div[id="j_id_3k_1:comboEscritorio_panel"]'

        self.message = "Informando Escritório Externo"
        self.type_log = "log"
        self.prt()

        div_escritrorioexterno: WebElement = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, escritrorioexterno)),
            message="Erro ao encontrar elemento",
        )
        div_escritrorioexterno.click()
        sleep(1)

        text = self.bot_data.get("ESCRITORIO_EXTERNO")
        self.interact.select_item(elemento, text)
        self.interact.sleep_load('div[id="j_id_3x"]')

        self.message = "Escritório externo informado!"
        self.type_log = "info"
        self.prt()

    def tipo_contingencia(self) -> None:
        """Declaração dos CSS em variáveis"""
        contingencia = (
            'div[id="j_id_3k_1:j_id_3k_4_2_2_s_9_n_1:processoContingenciaTipoCombo"]'
        )
        elemento = 'div[id="j_id_3k_1:j_id_3k_4_2_2_s_9_n_1:processoContingenciaTipoCombo_panel"]'

        text = "Passiva"
        if str(self.bot_data.get("TIPO_EMPRESA")).lower() == "autor":
            text = "Ativa"

        self.message = "Informando contingenciamento"
        self.type_log = "log"
        self.prt()

        div_contingencia: WebElement = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, contingencia)),
            message="Erro ao encontrar elemento",
        )
        div_contingencia.click()
        sleep(1)

        self.interact.select_item(elemento, text)
        self.interact.sleep_load('div[id="j_id_3x"]')

        self.message = "Contingenciamento informado!"
        self.type_log = "info"
        self.prt()

    def cad_adv(self) -> None:

        try:
            self.message = "Cadastrando advogado"
            self.type_log = "log"
            self.prt()

            css_add_adv = 'button[id="j_id_3k_1:lawyerOutraParteNovoButtom"]'
            add_parte: WebElement = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_add_adv)),
                message="Erro ao encontrar elemento",
            )
            add_parte.click()

            sleep(0.5)

            xpath = '//*[@id="j_id_3k_1:lawyerOutraParteNovoButtom_dlg"]/div[2]/iframe'

            iframe: WebElement = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath)),
                message="Erro ao encontrar elemento",
            )

            self.driver.switch_to.frame(iframe)

            sleep(0.5)

            css_naoinfomadoc = "#cpfCnpjNoGrid-lawyerOutraParte > tbody > tr > td:nth-child(1) > div > div.ui-radiobutton-box.ui-widget.ui-corner-all.ui-state-default"
            naoinfomadoc: WebElement = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_naoinfomadoc)),
                message="Erro ao encontrar elemento",
            )
            naoinfomadoc.click()

            sleep(0.5)
            continuebutton: WebElement = self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'button[id="j_id_1e"]')
                ),
                message="Erro ao encontrar elemento",
            )
            continuebutton.click()

            sleep(0.5)

            css_input_nomeadv = 'input[id="j_id_1h:j_id_1k_2_5"]'
            input_nomeadv: WebElement = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_input_nomeadv)),
                message="Erro ao encontrar elemento",
            )
            input_nomeadv.click()
            self.interact.send_key(
                input_nomeadv, self.bot_data.get("ADV_PARTE_CONTRARIA")
            )

            self.driver.execute_script(
                f"document.querySelector('{css_input_nomeadv}').blur()"
            )

            salvarcss = 'button[id="lawyerOutraParteButtom"]'
            sleep(0.05)
            salvar: WebElement = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, salvarcss)),
                message="Erro ao encontrar elemento",
            )
            salvar.click()

            self.message = "Advogado cadastrado!"
            self.type_log = "info"
            self.prt()
            self.interact.sleep_load('div[id="j_id_3x"]')

        except Exception as e:
            raise ErroDeExecucao("Não foi possível cadastrar advogado", e)

    def cad_parte(self) -> None:

        try:
            self.message = "Cadastrando parte"
            self.type_log = "log"
            self.prt()

            add_parte: WebElement = self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        'button[id="j_id_3k_1:j_id_3k_4_2_2_5_9_9_1:parteContrariaMainGridBtnNovo"]',
                    )
                ),
                message="Erro ao encontrar elemento",
            )
            add_parte.click()

            self.interact.sleep_load('div[id="j_id_3x"]')

            iframe = None

            xpath_iframe = '//*[@id="j_id_3k_1:j_id_3k_4_2_2_5_9_9_1:parteContrariaMainGridBtnNovo_dlg"]/div[2]/iframe'

            iframe: WebElement = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath_iframe)),
                message="Erro ao encontrar elemento",
            )

            self.driver.switch_to.frame(iframe)

            with suppress(TimeoutException, NoSuchElementException):
                set_infomar_cpf: WebElement = (
                    self.wait.until(
                        EC.presence_of_element_located(
                            (
                                By.CSS_SELECTOR,
                                'table[id="registrationCpfCnpjChooseGrid-"]',
                            )
                        ),
                        message="Erro ao encontrar elemento",
                    )
                    .find_elements(By.TAG_NAME, "td")[1]
                    .find_elements(
                        By.CSS_SELECTOR, 'div[class="ui-radiobutton ui-widget"]'
                    )[1]
                )

                set_infomar_cpf.click()

            table_tipo_doc: WebElement = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'table[id="cpfCnpjTipoNoGrid-"]')
                ),
                message="Erro ao encontrar elemento",
            )
            itensintotable = table_tipo_doc.find_elements(By.TAG_NAME, "td")

            sleep(0.5)

            for item in itensintotable:
                check_tipo = item.find_element(By.TAG_NAME, "label").text

                numero = "".join(
                    filter(str.isdigit, self.bot_data.get("DOC_PARTE_CONTRARIA"))
                )

                if len(numero) == 11:
                    tipo_doc = "cpf"

                elif len(numero) == 14:
                    tipo_doc = "cnpj"

                if check_tipo.lower() == tipo_doc:
                    select_tipo = item.find_element(
                        By.CSS_SELECTOR, 'div[class="ui-radiobutton ui-widget"]'
                    )
                    sleep(0.5)
                    select_tipo.click()
                    break

            self.interact.sleep_load('div[id="j_id_3x"]')

            if tipo_doc == "cpf":
                css_input_doc = 'input[id="j_id_19"]'

            elif tipo_doc == "cnpj":
                css_input_doc = 'input[id="j_id_1a"]'

            input_doc: WebElement = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_input_doc)),
                message="Erro ao encontrar elemento",
            )
            input_doc.click()
            sleep(0.05)
            input_doc.clear()
            self.interact.send_key(input_doc, self.bot_data.get("DOC_PARTE_CONTRARIA"))
            continuar = self.driver.find_element(
                By.CSS_SELECTOR, 'button[id="j_id_1d"]'
            )
            continuar.click()

            self.interact.sleep_load('div[id="j_id_3x"]')
            css_name_parte = 'input[id="j_id_1k"]'
            name_parte: WebElement = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_name_parte)),
                message="Erro ao encontrar elemento",
            )
            name_parte.click()
            sleep(0.05)
            self.interact.send_key(
                name_parte, self.bot_data.get("PARTE_CONTRARIA").__str__().upper()
            )
            self.driver.execute_script(
                f"document.querySelector('{css_name_parte}').blur()"
            )

            css_save_button = 'button[id="parteContrariaButtom"]'
            save_parte: WebElement = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_save_button)),
                message="Erro ao encontrar elemento",
            )
            save_parte.click()

            self.message = "Parte cadastrada!"
            self.type_log = "info"
            self.prt()

        except Exception as e:
            raise ErroDeExecucao(e=e)

    def salvar_tudo(self) -> None:

        self.interact.sleep_load('div[id="j_id_3x"]')
        css_salvar_proc = 'button[id="btnSalvarOpen"]'
        salvartudo: WebElement = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_salvar_proc)),
            message="Erro ao encontrar elemento",
        )

        self.message = "Salvando processo novo"
        self.type_log = "info"
        self.prt()

        salvartudo.click()

    def print_comprovante(self) -> None:

        name_comprovante = f'Comprovante Cadastro - {self.bot_data.get("NUMERO_PROCESSO")} - PID {self.pid}.png'
        savecomprovante = os.path.join(os.getcwd(), "Temp", self.pid, name_comprovante)
        self.driver.get_screenshot_as_file(savecomprovante)
        self.append_success(
            [self.bot_data.get("NUMERO_PROCESSO"), name_comprovante, self.pid]
        )

    def check_part_found(self, driver) -> str | None:

        css_t_found = 'table[id="j_id_3k_1:j_id_3k_4_2_2_5_9_9_1:parteContrariaSearchDisplayGrid"]'
        name_parte = ""
        with suppress(NoSuchElementException):
            name_parte = (
                self.driver.find_element(By.CSS_SELECTOR, css_t_found)
                .find_element(By.TAG_NAME, "td")
                .text
            )

        if name_parte != "":

            return name_parte

        return None

    def confirm_save(self) -> bool:

        wait_confirm_save = None

        with suppress(TimeoutException):
            wait_confirm_save: WebElement = WebDriverWait(self.driver, 20).until(
                EC.url_to_be(("https://amazonas.elaw.com.br/processoView.elaw")),
                message="Erro ao encontrar elemento",
            )

        if wait_confirm_save:

            self.message = "Processo salvo com sucesso!"
            self.type_log = "log"
            self.prt()
            return True

        elif not wait_confirm_save:
            div_messageerro_css = 'div[id="messages"]'
            ErroElaw: WebElement | str = None
            with suppress(TimeoutException, NoSuchElementException):
                ErroElaw = (
                    self.wait.until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, div_messageerro_css)
                        ),
                        message="Erro ao encontrar elemento",
                    )
                    .find_element(By.TAG_NAME, "ul")
                    .text
                )

            if not ErroElaw:
                ErroElaw = "Cadastro do processo nao finalizado, verificar manualmente"

            raise ErroDeExecucao(ErroElaw)
