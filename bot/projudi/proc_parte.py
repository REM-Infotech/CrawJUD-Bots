import os
import re
import time
from typing import Type
from datetime import datetime
from contextlib import suppress

""" Imports do Projeto """


from bot.head.common.exceptions import ErroDeExecucao

# Selenium Imports
# Selenium Imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement
from bot.head.common.exceptions import ErroDeExecucao
from selenium.webdriver.support import expected_conditions as EC
from bot.head.common.exceptions import ErroDeExecucao
from selenium.common.exceptions import NoSuchElementException

from bot.head import CrawJUD


class proc_parte(CrawJUD):

    def __init__(self, Initbot: Type[CrawJUD]) -> None:
        
        self.__dict__ = Initbot.__dict__.copy()
        self.start_time = time.perf_counter()
        
    def execution(self) -> None:
        
        while not self.thread._is_stopped:
            
            if self.driver.title.lower() == "a sessao expirou":
                self.auth(self)
            
            try:
                self.queue()
                
            except Exception as e:
                
                old_message = self.message
                message_error = str(e)
                
                self.type_log = "error"
                self.message_error = f'{message_error}. | Operação: {old_message}'
                self.prt(self)
                
                self.bot_data.update({"MOTIVO_ERRO": self.message_error})
                self.append_error(self.bot_data)
                
                self.message_error = None

        self.finalize_execution()
        
    def queue(self) -> None:
        
        search = self.search(self)
        if search is True:
            self.get_process_list()

            
    def get_process_list(self) -> None:

        try:
            table_processos = self.driver.find_element(By.CLASS_NAME, 'resultTable').find_element(By.TAG_NAME, 'tbody')

            list_processos = None
            next_page = None
            with suppress(NoSuchElementException):
                list_processos = table_processos.find_elements(By.XPATH, './/tr[contains(@class, "odd") or contains(@class, "even")]')
                
            if list_processos and not self.thread._is_stopped:
                self.use_list_process(list_processos)
                
                with suppress(NoSuchElementException):
                    next_page = self.driver.find_element(By.CLASS_NAME, 'navRight').find_element(By.XPATH, './/a[@class="arrowNextOn"]')
                
                self.append_success(data2=self.data_append, fileN=os.path.basename(self.path))
                if next_page:
                    next_page.click()
                    self.get_process_list()
                    
        except Exception as e:
            raise e

    def use_list_process(self, list_processos: list[WebElement]):
        
        self.data_append.clear()
        for processo in list_processos:
            numero_processo = processo.find_elements(By.TAG_NAME, 'td')[1].text
            
            numero = ''.join(filter(str.isdigit, numero_processo))
            anoref = ""
            if numero:
                anoref = numero_processo.split('.')[1]
                
            try:
                polo_ativo = processo.find_elements(By.TAG_NAME, 'td')[2].find_elements(By.TAG_NAME, 'td')[1].text
            except:
                polo_ativo = 'Não consta ou processo em sigilo'
                
            try:  
                polo_passivo = processo.find_elements(By.TAG_NAME, 'td')[7].text
            except:
                polo_passivo = 'Não consta ou processo em sigilo'
                
            try:  
                juizo = processo.find_elements(By.TAG_NAME, 'td')[9].text
            except: juizo = 'Não consta ou processo em sigilo'    


            self.data_append.append(
                {"NUMERO_PROCESSO": numero_processo,
                 "ANO_REFERENCIA": anoref,
                 "POLO_ATIVO": polo_ativo,
                 "POLO_PASSIVO": polo_passivo,
                 "JUIZO": juizo}
            )
            self.message = f"Processo {numero_processo} salvo!"
            self.type_log = "log"
            self.prt(self)





