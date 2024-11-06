""" Imports do Projeto """

from bot.CrawJUD import CrawJUD
from bot.Utils.count_doc import count_doc
import time
import requests
import platform
from PyPDF2 import PdfReader
import re
from time import sleep
from contextlib import suppress
from bot.common.exceptions import ErroDeExecucao
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

type_docscss = {
    "custas_iniciais": {
        "cnpj": [
            'input[name="entity.flTipoPessoa"][value="J"]',
            'tr[id="campoNuCnpj"]',
            'input[name="entity.nuCpfCnpj"][rotulo="CNPJ"]',
        ],
        "cpf": [
            'input[name="entity.flTipoPessoa"][value="F"]',
            'tr[id="campoNuCpf"]',
            'input[name="entity.nuCpfCnpj"][rotulo="CPF"]',
        ],
    },
    "preparo ri": {
        "cnpj": [
            'input[name="entity.flTipoPessoa"][value="J"]',
            'tr[id="campoNuCnpj"]',
            'input[name="entity.nuCpfCnpj"][rotulo="CNPJ"]',
        ],
        "cpf": [
            'input[name="entity.flTipoPessoa"][value="F"]',
            'tr[id="campoNuCpf"]',
            'input[name="entity.nuCpfCnpj"][rotulo="CPF"]',
        ],
    },
}


class emissao(CrawJUD):

    def __init__(self, **kwrgs) -> None:
        super().__init__(**kwrgs)
        super().auth_bot()
        self.start_time = time.perf_counter()

    def execution(self) -> None:

        frame = self.dataFrame()
        self.max_rows = len(frame)

        for pos, value in enumerate(frame):

            self.row = pos + 2
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

        try:
            custa = str(self.bot_data.get("TIPO_GUIA"))
            if custa.lower() == "custas iniciais":
                self.tipodoc = custa
                self.custas_iniciais()

            elif custa.lower() == "preparo ri":
                custa = "Custas Preparo"
                self.tipodoc = custa
                self.preparo_ri()

            self.downloadpdf(self.generate_doc())
            self.append_success(self.get_barcode())

        except Exception as e:
            raise ErroDeExecucao(e=e)

    def custas_iniciais(self) -> None:

        self.driver.get(
            "https://consultasaj.tjam.jus.br/ccpweb/iniciarCalculoDeCustas.do?cdTipoCusta=7&flTipoCusta=0&&cdServicoCalculoCusta=690003"
        )

        self.message = "Informando foro"
        self.type_log = "log"
        self.prt()

        set_foro: WebElement = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.elements.ome_foro))
        )
        set_foro.send_keys(self.bot_data.get("FORO"))

        set_classe = self.driver.find_element(
            By.CSS_SELECTOR, self.elements.tree_selection
        )
        set_classe.send_keys(self.bot_data.get("CLASSE"))

        semprecível = self.driver.find_element(
            By.CSS_SELECTOR, self.elements.civil_selector
        )
        semprecível.click()

        val_acao = self.driver.find_element(By.CSS_SELECTOR, self.elements.valor_acao)
        val_acao.send_keys(self.bot_data.get("VALOR_CAUSA"))

        nameinteressado = self.driver.find_element(
            By.CSS_SELECTOR, 'input[name="entity.nmInteressado"]'
        )
        nameinteressado.send_keys(self.bot_data.get("NOME_INTERESSADO"))

        elements: list = type_docscss.get(self.bot_data.get("TIPO_GUIA")).get(
            count_doc(self.bot_data.get("CPF_CNPJ"))
        )
        set_doc = self.driver.find_element(By.CSS_SELECTOR, elements[0])
        set_doc.click()
        sleep(0.5)
        setcpf_cnpj = self.driver.find_element(
            By.CSS_SELECTOR, elements[1]
        ).find_element(By.CSS_SELECTOR, elements[2])
        sleep(0.5)
        setcpf_cnpj.send_keys(self.bot_data.get("CPF_CNPJ"))

        avançar = self.driver.find_element(By.CSS_SELECTOR, self.elements.botao_avancar)
        avançar.click()

        self.valor_doc = ""
        with suppress(TimeoutException):
            css_val_doc = "body > table:nth-child(4) > tbody > tr > td > table:nth-child(10) > tbody > tr:nth-child(5) > td:nth-child(3) > strong"
            self.valor_doc: WebElement = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_val_doc))
            ).text

    def preparo_ri(self) -> None:

        portal = self.bot_data.get("PORTAL", "não informado")
        if str(portal).lower() == "esaj":
            self.driver.get(
                "https://consultasaj.tjam.jus.br/ccpweb/iniciarCalculoDeCustas.do?cdTipoCusta=9&flTipoCusta=1&&cdServicoCalculoCusta=690019"
            )

        elif str(portal).lower() == "projudi":
            self.driver.get(
                "https://consultasaj.tjam.jus.br/ccpweb/iniciarCalculoDeCustas.do?cdTipoCusta=21&flTipoCusta=5&&cdServicoCalculoCusta=690007"
            )

            set_foro: WebElement = self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, self.elements.nome_foro)
                )
            )
            set_foro.send_keys(self.bot_data.get("FORO"))

            val_acao = self.driver.find_element(
                By.CSS_SELECTOR, self.elements.valor_acao
            )
            val_acao.send_keys(self.bot_data.get("VALOR_CAUSA"))

            nameinteressado = self.driver.find_element(
                By.CSS_SELECTOR, self.elements.interessado
            )
            nameinteressado.send_keys(self.bot_data.get("NOME_INTERESSADO"))

            elements: list = type_docscss.get(self.bot_data.get("TIPO_GUIA")).get(
                count_doc(self.bot_data.get("CPF_CNPJ"))
            )

            set_doc = self.driver.find_element(By.CSS_SELECTOR, elements[0])
            set_doc.click()
            sleep(0.5)
            setcpf_cnpj = self.driver.find_element(
                By.CSS_SELECTOR, elements[1]
            ).find_element(By.CSS_SELECTOR, elements[2])
            sleep(0.5)
            setcpf_cnpj.send_keys(self.bot_data.get("CPF_CNPJ"))

            avançar = self.driver.find_element(
                By.CSS_SELECTOR, self.elements.botao_avancar
            )
            avançar.click()

            sleep(1)
            set_RI: WebElement = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.elements.check))
            )
            set_RI.click()

            sleep(1)
            last_avançar = self.driver.find_element(
                By.CSS_SELECTOR, self.elements.botao_avancar_dois
            )
            last_avançar.click()

            sleep(1)
            css_val_doc = "body > table:nth-child(4) > tbody > tr > td > table:nth-child(10) > tbody > tr:nth-child(3) > td:nth-child(3) > strong"
            self.valor_doc: WebElement = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_val_doc))
            ).text

        elif portal == "não informado":
            raise ErroDeExecucao(
                "Informar portal do processo na planilha (PROJUDI ou ESAJ)"
            )

    def renajud(self) -> None:
        pass

    def sisbajud(self) -> None:
        pass

    def custas_postais(self) -> None:
        pass

    def generate_doc(self) -> str:

        self.original_window = original_window = self.driver.current_window_handle
        generatepdf: WebElement = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.elements.boleto))
        )
        onclick_value = generatepdf.get_attribute("onclick")
        url_start = onclick_value.find("'") + 1
        url_end = onclick_value.find("'", url_start)
        url = onclick_value[url_start:url_end]
        sleep(0.5)
        # Store the ID of the original window

        sleep(0.5)
        self.driver.switch_to.new_window("tab")
        self.driver.get(f"https://consultasaj.tjam.jus.br{url}")
        sleep(2)

        # Checar se não ocorreu o erro "Boleto inexistente"
        check = None
        with suppress(TimeoutException):
            check: WebElement = (
                WebDriverWait(self.driver, 3)
                .until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, self.elements.mensagem_retorno)
                    )
                )
                .text
            )

        if check:
            self.driver.close()
            sleep(0.7)
            self.driver.switch_to.window(original_window)
            raise ErroDeExecucao("Esaj não gerou a guia")

        elif not check:
            return f"https://consultasaj.tjam.jus.br{url}"

    def downloadpdf(self, link_pdf):

        response = requests.get(link_pdf)

        self.nomearquivo = f"{self.tipodoc} - {self.bot_data.get('NUMERO_PROCESSO')} - {self.nomeparte} - {self.pid}.pdf"

        if platform.system() == "Windows":
            self.path_pdf = path_pdf = f"{self.output_dir_path}\\{self.nomearquivo}"

        elif platform.system() == "Linux":
            self.path_pdf = path_pdf = f"{self.output_dir_path}/{self.nomearquivo}"

        with open(path_pdf, "wb") as file:
            file.write(response.content)

        self.driver.close()
        sleep(0.7)
        self.driver.switch_to.window(self.original_window)
        self.message = (
            f"Boleto Nº{self.bot_data.get('NUMERO_PROCESSO')} emitido com sucesso!"
        )
        self.type_log = "log"
        self.prt()

    def get_barcode(self) -> None:

        try:
            self.message = "Extraindo código de barras"
            self.type_log = "log"
            self.prt()

            sleep(2)
            # Inicialize uma lista para armazenar os números encontrados
            bar_code = ""
            numeros_encontrados = []

            # Expressão regular para encontrar números nesse formato
            pattern = r"\b\d{5}\.\d{5}\s*\d{5}\.\d{6}\s*\d{5}\.\d{6}\s*\d\s*\d{14}\b"

            pdf_file = self.path_pdf
            read = PdfReader(pdf_file)

            # Read PDF
            for page in read.pages:
                text = page.extract_text()

                # Use a expressão regular para encontrar números
                numeros = re.findall(pattern, text)

                # Adicione os números encontrados à lista
                numeros_encontrados.extend(numeros)

            # Imprima os números encontrados
            for numero in numeros_encontrados:
                bar_code = numero.replace("  ", "")
                bar_code = bar_code.replace(" ", "")
                bar_code = bar_code.replace(".", " ")
                numero = numero.split("  ")
                numero = numero[2].split(".")

            return [
                self.bot_data.get("NUMERO_PROCESSO"),
                self.tipodoc,
                self.valor_doc,
                self.data_lancamento,
                "guias",
                "JEC",
                "SENTENÇA",
                bar_code,
                self.nomearquivo,
            ]

        except Exception as e:
            raise ErroDeExecucao(e=e)
