import os
import time
from contextlib import suppress


# Selenium Imports
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from bot.common.exceptions import ErroDeExecucao
from selenium.common.exceptions import NoSuchElementException

from bot.CrawJUD import CrawJUD


class proc_parte(CrawJUD):

    def __init__(self, **kwrgs) -> None:
        super().__init__(**kwrgs)
        super().auth_bot()
        self.start_time = time.perf_counter()
        self.data_append = []

    def execution(self) -> None:

        self.graphicMode = "bar"
        while not self.isStoped:

            if self.driver.title.lower() == "a sessao expirou":
                self.auth(self)

            try:
                self.queue()

            except Exception as e:

                old = self.message
                message_error = str(e)

                self.type_log = "error"
                self.message_error = f"{message_error}. | Operação: {old}"
                self.prt()

                self.bot_data.update({"MOTIVO_ERRO": self.message_error})
                self.append_error(self.bot_data)

                self.message_error = None

        self.finalize_execution()

    def queue(self) -> None:

        try:
            for vara in self.varas:
                self.vara: str = vara
                search = self.search()
                if search is True:
                    self.get_process_list()

        except Exception as e:
            raise ErroDeExecucao(e=e)

    def get_process_list(self) -> None:

        try:
            table_processos = self.driver.find_element(
                By.CLASS_NAME, "resultTable"
            ).find_element(By.TAG_NAME, "tbody")

            list_processos = None
            next_page = None
            with suppress(NoSuchElementException):
                list_processos = table_processos.find_elements(
                    By.XPATH,
                    self.elements.list_processos,
                )

            if list_processos and not self.isStoped:
                self.use_list_process(list_processos)

                with suppress(NoSuchElementException):
                    next_page = self.driver.find_element(
                        By.CLASS_NAME, "navRight"
                    ).find_element(By.XPATH, './/a[@class="arrowNextOn"]')

                self.type_log = "info"
                self.append_success(
                    self.data_append,
                    "Processos salvos na planilha!",
                    fileN=os.path.basename(self.path),
                )
                if next_page:
                    next_page.click()
                    self.get_process_list()

        except Exception as e:
            raise e

    def use_list_process(self, list_processos: list[WebElement]):

        self.data_append.clear()
        for processo in list_processos:
            numero_processo = processo.find_elements(By.TAG_NAME, "td")[1].text

            numero = "".join(filter(str.isdigit, numero_processo))
            anoref = ""
            if numero:
                anoref = numero_processo.split(".")[1]

            try:
                polo_ativo = (
                    processo.find_elements(By.TAG_NAME, "td")[2]
                    .find_elements(By.TAG_NAME, "td")[1]
                    .text
                )
            except Exception:
                polo_ativo = "Não consta ou processo em sigilo"

            try:
                polo_passivo = processo.find_elements(By.TAG_NAME, "td")[7].text

            except Exception:
                polo_passivo = "Não consta ou processo em sigilo"

            try:
                juizo = processo.find_elements(By.TAG_NAME, "td")[9].text
            except Exception:
                juizo = "Não consta ou processo em sigilo"

            self.data_append.append(
                {
                    "NUMERO_PROCESSO": numero_processo,
                    "ANO_REFERENCIA": anoref,
                    "POLO_ATIVO": polo_ativo,
                    "POLO_PASSIVO": polo_passivo,
                    "JUIZO": juizo,
                }
            )
            self.row += 1
            self.message = f"Processo {numero_processo} salvo!"
            self.type_log = "success"
            self.prt()
