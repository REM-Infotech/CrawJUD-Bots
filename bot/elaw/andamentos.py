""" Crawler ELAW Andamentos"""

import os
import time
from time import sleep
from typing import Type
from contextlib import suppress
import unicodedata

""" Imports do Projeto """
from bot.head import CrawJUD

from bot.head.Tools.PrintLogs import printtext as prt
from bot.head.common.exceptions import ErroDeExecucao
from bot.head.common.selenium_excepts import webdriver_exepts
from bot.head.common.selenium_excepts import exeption_message


# Selenium Imports
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import  NoSuchElementException, TimeoutException


class andamentos(CrawJUD):

    def __init__(self, Initbot: Type[CrawJUD]) -> None:
        
        self.__dict__ = Initbot.__dict__.copy()
        self.start_time = time.perf_counter()
        
    def execution(self):
        
        while not self.thread._is_stopped:
            if self.row == self.ws.max_row+1:
                self.prt = prt(self.pid, self.row)
                break
            self.prt = prt(self.pid, self.row-1)
            self.bot_data = {}
            for index in range(1, self.ws.max_column + 1):
                self.index = index
                self.bot_data.update(self.set_data())
                if index == self.ws.max_column:
                    break
            
            try:
                
                if not len(self.bot_data) == 0:
                    self.prt = prt(self.pid, self.row-1, url_socket=self.argbot['url_socket'])
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
                    
                error_message = f'{self.message}. | Operação: {old_message}'
                self.prt.print_log("error", error_message)
                self.append_error([self.bot_data.get('NUMERO_PROCESSO'), self.message])
            
            self.row += 1
            
        self.finalize_execution()

        
    def queue(self):
        
        search = self.search(self.bot_data, self.prt)
        if search is True:
            btn_newmove = 'button[id="tabViewProcesso:j_id_i3_4_1_3_ae:novoAndamentoPrimeiraBtn"]'
            new_move: WebElement = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, btn_newmove)))
            new_move.click()
            
            self.info_data()
            self.info_ocorrencia()
            self.info_observacao()
            
            if self.bot_data.get("ANEXOS", None):
                    self.add_anexo()

            self.save_andamento()
            
        else:
            self.message = "Processo não encontrado!"
            self.prt.print_log("error", self.message)
            self.append_error([self.bot_data.get("NUMERO_PROCESSO"), self.message])

  
    def info_data(self):

        try:
            
            self.prt.print_log("log", "Informando data")
            css_Data = 'input[id="j_id_2n:j_id_2r_2_9_input"]'
            campo_data: WebElement = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_Data)))
            campo_data.click()
            campo_data.send_keys(Keys.CONTROL, 'a')
            sleep(0.5)
            campo_data.send_keys(Keys.BACKSPACE)
            self.interact.send_key(campo_data, self.bot_data.get("DATA"))
            campo_data.send_keys(Keys.TAB)
            
            self.interact.sleep_load('div[id="j_id_34"]')
            
        except Exception as e:
            raise ErroDeExecucao()
        
    def info_ocorrencia(self):
        
        try:
            self.prt.print_log('log', "Informando ocorrência")
            
            inpt_ocorrencia = 'textarea[id="j_id_2n:txtOcorrenciaAndamento"]'
            
            ocorrencia = self.driver.find_element(By.CSS_SELECTOR, inpt_ocorrencia)
            text_andamento = str(self.bot_data.get("OCORRENCIA")).replace("\t","").replace("\n", "")
            
            self.interact.send_key(ocorrencia, text_andamento)

        except Exception as e:
            raise ErroDeExecucao()
    
    def info_observacao(self):
        
        try:
            self.prt.print_log('log', "Informando observação")
            
            inpt_obs = 'textarea[id="j_id_2n:txtObsAndamento"]'
            
            observacao = self.driver.find_element(By.CSS_SELECTOR, inpt_obs)
            text_andamento = str(self.bot_data.get("OBSERVACAO")).replace("\t","").replace("\n", "")
            
            self.interact.send_key(observacao, text_andamento)

        except Exception as e:
            raise ErroDeExecucao()
    
    def add_anexo(self):

        pass
            
    def save_andamento(self):
        
        try:
            self.prt.print_log('log', 'Salvando andamento...')
            sleep(1)
            self.link = self.driver.current_url
            save_button = self.driver.find_element(By.ID, 'btnSalvarAndamentoProcesso')
            save_button.click()
            
            
        except Exception  as e:
            self.message = f'Não foi possivel salvar andamento'
            raise ErroDeExecucao(self.message)
 
        try:
            check_save:WebElement = WebDriverWait(self.driver, 10).until(EC.url_to_be('https://amazonas.elaw.com.br/processoView.elaw'))
            if check_save:
                sleep(3)
                self.prt.print_log('log', 'Andamento salvo com sucesso!')
                self.append_sucess(numprocesso=[self.numproc])
                
        except:
            self.message = "Aviso: não foi possivel validar salvamento de andamento"
            raise ErroDeExecucao(self.message)
