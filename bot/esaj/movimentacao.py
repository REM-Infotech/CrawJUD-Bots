import time
from time import sleep
from typing import Type
from contextlib import suppress
from datetime import datetime

""" Imports do Projeto """
from bot.head import CrawJUD


from bot.head.common.selenium_excepts import webdriver_exepts
from bot.head.common.selenium_excepts import exeption_message
from bot.head.common.exceptions import ErroDeExecucao

# Selenium Imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import  TimeoutException

class movimentacao(CrawJUD):

    def __init__(self, Initbot: Type[CrawJUD]) -> None:
        
        self.__dict__ = Initbot.__dict__.copy()
        
    def execution(self):
        
        frame = self.dataFrame()
        self.max_rows = len(frame)
        
        for pos, value in enumerate(frame):
            
            self.row = pos+2
            self.bot_data = value
            if self.thread._is_stopped:
                break
            
            if self.driver.title.lower() == "a sessao expirou":
                self.auth(self)
            
            try:
                self.queue()
                
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
                self.bot_data.update({"MOTIVO_ERRO": self.message_error})
                self.append_error(self.bot_data)
                self.message_error = None

        self.finalize_execution()
        
    def queue(self) -> None:
        
        self.appends = []
        self.resultados = []
        
        self.search(self)
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
            table_moves = self.driver.find_element(By.CSS_SELECTOR, movimentacoes)
            self.driver.execute_script('document.querySelector("#tabelaTodasMovimentacoes").style.display = "block"')
        except:
            table_moves = self.driver.find_element(By.ID, ultimas_movimentacoes)
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

