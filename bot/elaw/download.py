""" Crawler ELAW Baixa Documentos"""

import os
import time
import shutil
from time import sleep
from typing import Type
from contextlib import suppress


""" Imports do Projeto """
from bot.head import CrawJUD


from bot.head.common.exceptions import ErroDeExecucao
from bot.head.common.selenium_excepts import webdriver_exepts
from bot.head.common.selenium_excepts import exeption_message


# Selenium Imports
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import  NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC


class download(CrawJUD):

    def __init__(self, Initbot: Type[CrawJUD]) -> None:
        
        self.__dict__ = Initbot.__dict__.copy()
        self.start_time = time.perf_counter()
        
    def execution(self):
        
        while not self.thread._is_stopped:
            
            if self.row == self.ws.max_row+1:
                self.row = self.ws.max_row+1
                break
            
            self.list_docs = None
            self.bot_data = {}
            for index in range(1, self.ws.max_column + 1):
                self.index = index
                self.bot_data.update(self.set_data())
                if index == self.ws.max_column:
                    break
            
            try:
                
                if not len(self.bot_data) == 0:
                    self.queue()
                
            except Exception as e:
                
                old_message = self.message
                message_error = getattr(e, 'msg', getattr(e, 'message', ""))
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
                self.bot_data.update({'MOTIVO_ERRO': self.message_error})
                self.append_error(data=self.bot_data)
                self.message_error = None
            
            self.row += 1
            
        self.finalize_execution()

    def queue(self) -> None:
        
        check_cadastro = self.search(self)
        if check_cadastro is True:
        
            self.message = 'Processo encontrado!'
            self.type_log = "log"
            self.prt(self)
            self.buscar_doc()
            self.download_docs()
            self.message = 'Arquivos salvos com sucesso!'
            self.append_success([self.bot_data.get("NUMERO_PROCESSO"), self.message, self.list_docs], 'Arquivos salvos com sucesso!')
            
        elif not check_cadastro:
            self.message = "Processo não encontrado!"
            self.type_log = "error"
            self.prt(self)
            self.append_error([self.bot_data.get("NUMERO_PROCESSO"), self.message])
        
    def buscar_doc(self):
          
        self.message = "Acessando página de anexos"
        self.type_log = "log"
        self.prt(self)
        anexosbutton_css = 'a[href="#tabViewProcesso:files"]'
        anexosbutton: WebElement = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, anexosbutton_css)))
        anexosbutton.click()
        sleep(1.5)
        self.message = "Acessando tabela de documentos"
        self.type_log = "log"
        self.prt(self)      
    
    def download_docs(self):
        
        css_table_doc = 'tbody[id="tabViewProcesso:gedEFileDataTable:GedEFileViewDt_data"]'
        table_doc: WebElement = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_table_doc)))
        table_doc = table_doc.find_elements(By.TAG_NAME, 'tr')
        
        if "," in self.bot_data.get("TERMOS"):
            termos = str(self.bot_data.get("TERMOS")).replace(", ", ",").replace(" ,", ",").split(",")
            
        elif not "," in self.bot_data.get("TERMOS"):
            termos = [str(self.bot_data.get("TERMOS"))]
        
        self.message = f'Buscando documentos que contenham "{self.bot_data.get("TERMOS").__str__().replace(",", ", ")}"'
        self.type_log = "log"
        self.prt(self)
        
        for item in table_doc:
            
            item: WebElement = item
            get_name_file = str(item.find_elements(By.TAG_NAME, 'td')[3].find_element(By.TAG_NAME, 'a').text)
            
            for termo in termos:
            
                if str(termo).lower() in get_name_file.lower():
                    sleep(1)
                    
                    self.message = f'Arquivo com termo de busca "{termo}" encontrado!'
                    self.type_log = "log"
                    self.prt(self)
                    
                    baixar = item.find_elements(By.TAG_NAME, 'td')[13].find_element(By.CSS_SELECTOR, 'button[title="Baixar"]')
                    baixar.click()
                              
                    self.rename_doc(get_name_file)
                    self.message = f'Arquivo baixado com sucesso!'
                    self.type_log = "log"
        self.prt(self)
    
    def rename_doc(self, namefile: str):
        
        filedownloaded = False
        while  True:
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