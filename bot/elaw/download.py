""" Crawler ELAW Baixa Documentos"""

import os
import time
import shutil
from time import sleep
from bot.CrawJUD import CrawJUD
from bot.common.exceptions import ErroDeExecucao


# Selenium Imports
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC


class download(CrawJUD):

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

        try:
            search = self.search()
            if search is True:

                self.message = "Processo encontrado!"
                self.type_log = "log"
                self.prt()
                self.buscar_doc()
                self.download_docs()
                self.message = "Arquivos salvos com sucesso!"
                self.append_success(
                    [
                        self.bot_data.get("NUMERO_PROCESSO"),
                        self.message,
                        self.list_docs,
                    ],
                    "Arquivos salvos com sucesso!",
                )

            elif not search:
                self.message = "Processo não encontrado!"
                self.type_log = "error"
                self.prt()
                self.append_error([self.bot_data.get("NUMERO_PROCESSO"), self.message])

        except Exception as e:
            raise ErroDeExecucao(e=e)

    def buscar_doc(self) -> None:

        self.message = "Acessando página de anexos"
        self.type_log = "log"
        self.prt()
        anexosbutton_css = 'a[href="#tabViewProcesso:files"]'
        anexosbutton: WebElement = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, anexosbutton_css))
        )
        anexosbutton.click()
        sleep(1.5)
        self.message = "Acessando tabela de documentos"
        self.type_log = "log"
        self.prt()

    def download_docs(self) -> None:

        css_table_doc = (
            'tbody[id="tabViewProcesso:gedEFileDataTable:GedEFileViewDt_data"]'
        )
        table_doc: WebElement = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_table_doc))
        )
        table_doc = table_doc.find_elements(By.TAG_NAME, "tr")

        if "," in self.bot_data.get("TERMOS"):
            termos = (
                str(self.bot_data.get("TERMOS"))
                .replace(", ", ",")
                .replace(" ,", ",")
                .split(",")
            )

        elif "," not in self.bot_data.get("TERMOS"):
            termos = [str(self.bot_data.get("TERMOS"))]

        self.message = f'Buscando documentos que contenham "{self.bot_data.get("TERMOS").__str__().replace(",", ", ")}"'
        self.type_log = "log"
        self.prt()

        for item in table_doc:

            item: WebElement = item
            get_name_file = str(
                item.find_elements(By.TAG_NAME, "td")[3]
                .find_element(By.TAG_NAME, "a")
                .text
            )

            for termo in termos:

                if str(termo).lower() in get_name_file.lower():
                    sleep(1)

                    self.message = f'Arquivo com termo de busca "{termo}" encontrado!'
                    self.type_log = "log"
                    self.prt()

                    baixar = item.find_elements(By.TAG_NAME, "td")[13].find_element(
                        By.CSS_SELECTOR, 'button[title="Baixar"]'
                    )
                    baixar.click()

                    self.rename_doc(get_name_file)
                    self.message = "Arquivo baixado com sucesso!"
                    self.type_log = "info"
                    self.prt()

    def rename_doc(self, namefile: str):

        filedownloaded = False
        while True:
            for root, dirs, files in os.walk(os.path.join(self.output_dir_path)):

                for file in files:

                    if file.replace(" ", "") == namefile.replace(" ", ""):

                        filedownloaded = True
                        namefile = file
                        break

                if filedownloaded is True:
                    break

            old_file = os.path.join(self.output_dir_path, namefile)
            if os.path.exists(old_file):
                sleep(0.5)
                break

            sleep(0.01)

        filename_replaced = f'{self.pid} - {namefile.replace(" ", "")}'
        path_renamed = os.path.join(self.output_dir_path, filename_replaced)
        shutil.move(old_file, path_renamed)

        if not self.list_docs:
            self.list_docs = filename_replaced

        elif self.list_docs:
            self.list_docs = self.list_docs + "," + filename_replaced
