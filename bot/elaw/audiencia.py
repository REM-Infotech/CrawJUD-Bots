import os
import time
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



class audiencia(CrawJUD):

    def __init__(self, Initbot: Type[CrawJUD]) -> None:
        
        self.__dict__ = Initbot.__dict__.copy()
        self.start_time = time.perf_counter()
        
    def execution(self) -> None:
        
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
        
        result = self.search(self)
        if result:
            
            self.message = "Processo Encontrado!"
            self.type_log = "log"
            self.prt(self)
            
            self.nova_audiencia()
            
            self.TipoAudiencia()
            self.dataAudiencia()
            self.save_Prazo()
            comprovante = self.GetComprovante()
            if not comprovante:
                raise ErroDeExecucao(
                    "Não foi possível comprovar lançamento, verificar manualmente")

            data = [{
                "NUMERO_PROCESSO": self.bot_data["NUMERO_PROCESSO"],
                "MENSAGEM_COMCLUSAO": f"PRAZO LANÇADO!. ID: {self.idPrazo}", 
                "NOME_COMPROVANTE": self.nameComprovante
            }]
            self.append_success(data)
            
    def nova_audiencia(self) -> None:

        try:
            self.message = "Lançando nova audiência"
            self.type_log = "log"
            self.prt(self)
            
            switch_pautaAndamento = self.driver.find_element(
                By.CSS_SELECTOR, self.elements.switch_pautaAndamento)
            
            switch_pautaAndamento.click()
            
            btn_NovaAudiencia = self.wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR, self.elements.btn_NovaAudiencia
            )))
            
            btn_NovaAudiencia.click()
            
        except Exception as e:
            raise ErroDeExecucao(str(e))
        
    def TipoAudiencia(self) -> None:
        
        try:
            self.message = "Informando tipo de audiência"
            self.type_log = "log"
            self.prt(self)
            
            selectorTipoAudiencia: WebElement = self.wait.until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, self.elements.selectorTipoAudiencia)))
            
            items = selectorTipoAudiencia.find_elements(By.TAG_NAME, "option")
            opt_itens: dict[str, str] = {}
            for item in items:
                opt_itens.update({item.text.upper(): item.get_attribute("value")})
            
            value_opt = opt_itens.get(self.bot_data["TIPO_AUDIENCIA"].upper())
            if value_opt:
                self.driver.execute_script(
                    f'$("{self.elements.selectorTipoAudiencia}").val(["{value_opt}"]);')
                
                self.driver.execute_script(
                    f'$("{self.elements.selectorTipoAudiencia}").trigger("change");')
                
        except Exception as e:
            raise ErroDeExecucao(str(e))
            
    def dataAudiencia(self) -> None:
        
        try:
            
            self.message = "Informando data da Audiência"
            self.type_log = "log"
            self.prt(self)
            
            DataAudiencia: WebElement = self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, self.elements.DataAudiencia)))
            
            self.data_Concat = f"{self.bot_data["DATA_AUDIENCIA"]} {self.bot_data["HORA_AUDIENCIA"]}"
            DataAudiencia.send_keys(self.data_Concat)
        
        except Exception as e:
            raise ErroDeExecucao(str(e))
        
    def save_Prazo(self) -> None:
        
        try:
            
            self.message = "Salvando..."
            self.type_log = "log"
            self.prt(self)
            
            btn_Salvar = self.driver.find_element(
                By.CSS_SELECTOR, self.elements.btn_Salvar)
            
            btn_Salvar.click()
            
        except Exception as e:
            raise ErroDeExecucao(str(e))
        
    def GetComprovante(self) -> bool:
        
        try:
            self.message = "Gerando comprovante"
            self.type_log = "log"
            self.prt(self)
            
            tablePrazos: WebElement = self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, self.elements.tablePrazos)))
            
            tablePrazos: list[WebElement] = tablePrazos.find_elements(
                By.TAG_NAME, "tr")
            
            comprovante = False
            for item in tablePrazos:
                
                data_Prazo = item.find_elements(
                    By.TAG_NAME, "td")[4]
                if data_Prazo == self.data_Concat:
                    nProc_pid = f'{self.bot_data["NUMERO_PROCESSO"]} - {self.pid}'
                    
                    self.nameComprovante = f"Comprovante - {nProc_pid}.png"
                    self.idPrazo = item.find_elements(By.TAG_NAME, "td")[2]
                    
                    comprovante = item.screenshot(
                        os.path.join(
                            self.output_dir_path, self.nameComprovante))
            
            return comprovante
        
        except Exception as e:
            raise ErroDeExecucao(str(e))

        