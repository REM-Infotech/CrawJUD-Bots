import time
from time import sleep
from typing import Type
from contextlib import suppress
from datetime import datetime

""" Imports do Projeto """
from Scripts.CrawJUD import CrawJUD
from Scripts.CrawJUD.search import SeachBot
from Scripts.Tools.PrintLogs import printtext as prt
from Scripts.common.selenium_excepts import webdriver_exepts
from Scripts.common.selenium_excepts import exeption_message
from Scripts.common.exceptions import ErroDeExecucao

# Selenium Imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import  TimeoutException

class EsajCrawlerMov(CrawJUD):
    
    def __init__(self, Initbot: Type[CrawJUD]) -> None:
        
        self.__dict__ = Initbot.__dict__.copy()

        self.search = SeachBot(self.driver, self.wait, self.portal).search
        
        self.start_time = time.perf_counter()

    def execution(self):
        
        while True:
            if self.row == self.ws.max_row+1:
                self.prt = prt(self.pid, self.row)
                break
            
            self.appends = []
            self.resultados = []
            self.prt = prt(self.pid, self.row-1)
            self.bot_data = {}
            for index in range(1, self.ws.max_column + 1):
                self.index = index
                self.bot_data.update(self.set_data())
                if index == self.ws.max_column:
                    break
            
            try:
                self.queue()
                
            except Exception as e:
                
                old_message = self.message
                self.message = getattr(e, 'msg', getattr(e, 'message', ""))
                if self.message == "":
                    for exept in webdriver_exepts():
                        if isinstance(e, exept):
                            self.message = exeption_message().get(exept)
                            break
                        
                if not self.message:
                    self.message = str(e)
                    
                self.message = f'{self.message}. | Operação: {old_message}'
                self.prt.print_log("error", self.message)
                self.append_error([self.bot_data.get('NUMERO_PROCESSO'), self.message])
            
            self.row += 1
            
        self.finalize_execution()
        
    def queue(self) -> None:
        
        self.search(self.bot_data, self.prt)
        self.get_moves()
        self.append_moves()
        
    def get_moves(self) -> None:
        
        show_all: WebElement = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[id="linkmovimentacoes"]')))
        
        self.interact.scroll_to(show_all)
        
        # Rolar até o elemento
        self.driver.execute_script("arguments[0].scrollIntoView(true);", show_all)

        # Use JavaScript para clicar no elemento
        self.driver.execute_script("arguments[0].click();", show_all)
        
        sleep(0.5)
        
        try: 
            table_moves = self.driver.find_element(By.CSS_SELECTOR, 'tbody[id="tabelaTodasMovimentacoes"]')
            self.driver.execute_script('document.querySelector("#tabelaTodasMovimentacoes").style.display = "block"')
        except:
            table_moves = self.driver.find_element(By.ID, 'tabelaUltimasMovimentacoes')
            self.driver.execute_script('document.querySelector("#tabelaUltimasMovimentacoes").style.display = "block"')
            
        itens = table_moves.find_elements(By.TAG_NAME, "tr")
        
        palavra_chave = str(self.bot_data.get("PALAVRA_CHAVE"))
        termos = [palavra_chave]
        
        if "," in palavra_chave:
            termos = palavra_chave.replace(", ", ",").split(",")
            
        for termo in termos:
            
            self.prt.print_log("log", f'Buscando movimentações que contenham "{termo}"')
            for item in itens:
                td_tr = item.find_elements(By.TAG_NAME, 'td')
                mov = td_tr[2].text
                
                if termo.lower() in mov.lower():
                    data_mov = td_tr[0].text
                    
                    try:
                        data_mov = datetime.strptime(data_mov.replace("/", "-"), "%d-%m-%Y")
                        
                    except Exception as e:
                        pass
                        
                    name_mov = mov.split("\n")[0]
                    text_mov = td_tr[2].find_element(By.TAG_NAME, 'span').text
                    self.appends.append([self.bot_data.get("NUMERO_PROCESSO"), data_mov, name_mov, text_mov, "", ""])

