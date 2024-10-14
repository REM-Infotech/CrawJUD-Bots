import os
import json
import time
import shutil
import random
import platform
import threading
import subprocess
from tqdm import tqdm
from time import sleep
from clear import clear
from typing import Type
from datetime import datetime
from datetime import timedelta
from contextlib import suppress


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

from bot.head import CrawJUD
from bot.head.common.selenium_excepts import webdriver_exepts
from bot.head.common.selenium_excepts import exeption_message
from bot.head.common.exceptions import ErroDeExecucao


class pauta(CrawJUD):

    def __init__(self, Initbot: Type[CrawJUD]) -> None:

        self.__dict__ = Initbot.__dict__.copy()
        self.start_time = time.perf_counter()
        self.data_append: list[
            dict[str, dict[str, list[dict[str, str]]]]] = {}

    def execution(self):

        self.row = 2
        while not self.thread._is_stopped:

            if self.row == self.total_rows+2:

                data_append = self.group_date_all(self.data_append)
                fileN = os.path.basename(self.path)
                self.append_success(pauta_data=data_append, fileN=fileN)
                break

            self.queue()
            self.row += 1

        self.finalize_execution()

    def queue(self):
        
        current_date = self.data_inicio + timedelta(days=self.row-2)
        self.message = f"Buscando pautas na data {current_date.strftime('%d/%m/%Y')}"
        self.type_log = "log"
        self.prt(self)
        
        for vara in self.varas:

            try:
                
                date = current_date.strftime('%Y-%m-%d')
                self.data_append.update({vara: {date: []}})

                # O filtro funciona conforme a URL. Veja o "varas_dict.py"
                # Defini conforme o TRT 11, atualize esse arquivo conforme seu estado
                # No TRT11, é "url/pautas{juizado}-{data_filtro}"

                # Exemplo: https://pje.trt11.jus.br/consultaprocessual/pautas#VTBV3-1-2024-07-24

                self.driver.get(f"{self.elements.url_pautas}{vara}-{date}")
                self.get_pautas(current_date, vara)

                if len(self.data_append[vara][date]) == 0:
                    self.data_append[vara].pop(date)

                data_append = self.group_date(self.data_append[vara], vara)
                if len(data_append) > 0:
                    self.append_success(pauta_data=data_append,
                                        fileN=f"{vara}_{date}.xlsx")
                
            except Exception as e:
                
                old_message = self.message
                message_error: str = getattr(e, 'msg', getattr(e, 'message', ""))
                if message_error == "":
                    for exept in webdriver_exepts():
                        if isinstance(e, exept):
                            message_error = exeption_message().get(exept)
                            break
                        
                if not message_error:
                    message_error = str(e)
                
                self.type_log = "error"
                self.message_error = f'{message_error}. | Operação: {old_message}'
                self.prt(self)
                self.append_error([vara, self.message])
                self.message_error = None
                
                
    def get_pautas(self, current_date: Type[datetime], vara: str):

        try:

            # Interage com a tabela de pautas
            self.driver.implicitly_wait(2)
            times = 4
            itens_pautas = None
            table_pautas: WebElement = self.wait.\
                until(EC.
                      all_of(EC.presence_of_element_located(
                          (By.CSS_SELECTOR, 'pje-data-table[id="tabelaResultado"]'))),
                      (EC.visibility_of_element_located(
                          (By.CSS_SELECTOR, 'table[name="Tabela de itens de pauta"]'))))[-1]

            with suppress(NoSuchElementException, TimeoutException):
                itens_pautas = table_pautas.find_element(
                    By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')

            # Caso encontre a tabela, raspa os dados
            if itens_pautas:

                self.meesage = "Pautas encontradas!"
                self.type_log = "log"
                self.prt(self)

                times = 6

                for item in itens_pautas:

                    with suppress(StaleElementReferenceException):
                        item: WebElement = item
                        itens_tr = item.find_elements(By.TAG_NAME, 'td')

                        appends = {"INDICE": itens_tr[0].text,
                                   "HORARIO": itens_tr[1].text,
                                   "TIPO": itens_tr[2].text,
                                   "NUMERO_PROCESSO": itens_tr[3].find_element(By.TAG_NAME, 'a').text,
                                   "PARTES": itens_tr[3].find_element(By.TAG_NAME, 'span').find_element(By.TAG_NAME, 'span').text,
                                   "SALA": itens_tr[5].text,
                                   "SITUACAO": itens_tr[6].text}

                        self.appends[vara][current_date].append(appends)
                        self.meesage = f"Processo {
                            appends["NUMERO_PROCESSO"]} adicionado!"
                        self.type_log = "log"
                        self.prt(self)

                try:
                    btn_next = self.driver.find_element(
                        By.CSS_SELECTOR, 'button[aria-label="Próxima página"]')

                    buttondisabled = btn_next.get_attribute("disabled")
                    if not buttondisabled:

                        btn_next.click()
                        self.get_pautas(current_date, vara)

                except Exception as e:
                    raise ErroDeExecucao(str(e))

            elif not itens_pautas:
                self.message = "Nenhuma pauta encontrada"
                self.type_log = "log"
                self.prt(self)
                times = 1
            # Eu defini um timer, um caso encontre a tabela e outro
            # para caso não encontre ela

            sleep(times)

        except Exception as e:
            raise ErroDeExecucao(str(e))

    def auth(self, usuario: str, senha: str, driver: WebDriver):

        wait = WebDriverWait(driver, 20)
        driver.get("https://pje.trt11.jus.br/primeirograu/login.seam")

        login = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'input[id="username"]')))
        password = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'input[id="password"]')))
        entrar = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'button[id="btnEntrar"]')))

        login.send_keys(usuario)
        sleep(0.5)
        password.send_keys(senha)
        sleep(0.5)
        entrar.click()

        logado = None
        with suppress(TimeoutException):
            logado = wait.until(EC.url_to_be(
                "https://pje.trt11.jus.br/pjekz/painel/usuario-externo"))

        if not logado:
            raise

    def group_date_all(self, data: dict[str, dict[str, str]]) -> dict[str, str]:

        for vara, dates in data.items():
            for date, entries in dates.items():
                for entry in entries:
                    record = {'Vara': vara, 'Data': date}
                    record.update(entry)

        return record

    def group_date(self, data: dict[list[str]], vara: str) -> dict[str, str]:

        record = {}
        for date, entries in data.items():
            for entry in entries:
                record = {'Vara': vara, 'Data': date}
                record.update(entry)

        return record
