import time
from time import sleep
from typing import Type
from contextlib import suppress


""" Imports do Projeto """
from Scripts.CrawJUD import CrawJUD
from Scripts.CrawJUD.search import SeachBot
from Scripts.Tools.PrintLogs import printtext as prt
from Scripts.common.selenium_excepts import webdriver_exepts
from Scripts.common.selenium_excepts import exeption_message


# Selenium Imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import  TimeoutException

class EsajCrawlerCapa(CrawJUD):
    
    def __init__(self, Initbot: Type[CrawJUD]) -> None:
        
        self.__dict__ = Initbot.__dict__.copy()

        self.search = SeachBot(self.driver, self.wait, self.portal).search
        
        self.start_time = time.perf_counter()
        
    def execution(self):
        
        while True:
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
        
        self.search(self.bot_data, self.prt)
        self.append_success(self.get_process_informations())
      
    def get_process_informations(self) -> list:
        
        self.message = f"Extraindo informações do processo nº{self.bot_data.get('NUMERO_PROCESSO')}"
        self.prt.print_log("log", self.message)
        
        grau = int(str(self.bot_data.get("GRAU")).replace("º", ""))
        if grau == 1:
            
            acao: WebElement = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[id="classeProcesso"]'))).text
            area_do_direito = "Diversos"
            if acao == "Procedimento do Juizado Especial Cível":
                area_do_direito = str(acao).replace("Procedimento do ", "")
                
            subarea_direito = "Geral"
            estado = "Amazonas"
            comarca = self.driver.find_element(By.ID, 'foroProcesso').text
            
            if "Fórum de " in comarca:
                comarca = str(comarca).replace("Fórum de ", "")
                
            vara: WebElement = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[id="varaProcesso"]'))).text.split(" ")[0]
            foro: WebElement = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[id="varaProcesso"]'))).text.replace(f"{vara} ", "")
            table_partes = self.driver.find_element(By.ID, 'tablePartesPrincipais')
            polo_ativo = table_partes.find_elements(By.TAG_NAME, 'tr')[0].find_elements(By.TAG_NAME, 'td')[1].text.split('\n')[0]
            tipo_parte = "Autor"
            cpf_polo_ativo = 'Não consta'
            polo_passivo = table_partes.find_elements(By.TAG_NAME, 'tr')[1].find_elements(By.TAG_NAME, 'td')[1].text.split('\n')[0]
            tipo_passivo = "réu"
            cpf_polo_passivo = 'Não consta'
            try:
                adv_polo_ativo = table_partes.find_elements(By.TAG_NAME, 'tr')[0].find_elements(By.TAG_NAME, 'td')[1].text.split(':')[1].replace('Advogado:','').replace('Advogada:','').replace("  ","")
            except:
                adv_polo_ativo = 'Não consta'
            escritorio_externo = "Fonseca Melo e Viana Advogados Associados"
            fase = "inicial"
            valor = ""
            with suppress(TimeoutException):
                valor:WebElement = WebDriverWait(self.driver, 1, 0.01).until(EC.presence_of_element_located((By.ID, 'valorAcaoProcesso'))).text
            
            def converte_valor_causa(valor_causa) -> str:
                if "R$" in valor_causa:
                    valor_causa = float(valor_causa.replace("$", "").replace("R", "").replace(" ", "").replace(".","").replace(",",".")) 
                    return "{:.2f}".format(valor_causa).replace(".", ",")
                    
                if not "R$" in valor_causa:
                    valor_causa = float(valor_causa.replace("$", "").replace("R", "").replace(" ", "").replace(",",""))
                    return "{:.2f}".format(valor_causa).replace(".", ",")
            
            valorDaCausa = valor
            if valor != "":
                valorDaCausa = converte_valor_causa(valor)  
            
            sleep(0.5)
            distnotformated: WebElement = self.wait.until(EC.presence_of_element_located((By.ID, 'dataHoraDistribuicaoProcesso'))).text.replace(' às ', '|').replace(' - ', '|')
            distdata = distnotformated.split('|')[0]
            processo_data = [self.bot_data.get('NUMERO_PROCESSO'), area_do_direito, subarea_direito, estado, comarca, foro, vara, 
                             distdata, polo_ativo, tipo_parte, cpf_polo_ativo, polo_passivo, tipo_passivo,
                             cpf_polo_passivo, "", "", "", acao, "" , "", "", "", adv_polo_ativo,
                             "", escritorio_externo, valorDaCausa, fase]
                            
        elif grau == 2:
            
            classe: WebElement = self.wait.until(EC.presence_of_element_located(((By.XPATH, '//*[@id="classeProcesso"]/span')))).text
            seção: WebElement = self.wait.until(EC.presence_of_element_located(((By.XPATH, '//*[@id="secaoProcesso"]/span')))).text
            julgador: WebElement = self.wait.until(EC.presence_of_element_located(((By.XPATH, '//*[@id="orgaoJulgadorProcesso"]')))).text
            try:
                situaçãoproc = self.driver.find_element(By.CSS_SELECTOR, 'span[id="situacaoProcesso"]').text
            except:
                situaçãoproc = 'Não Consta'
            relator: WebElement = self.wait.until(EC.presence_of_element_located(((By.XPATH, '//*[@id="relatorProcesso"]')))).text
            table_partes = self.driver.find_element(By.ID, 'tablePartesPrincipais')
            polo_ativo = table_partes.find_elements(By.TAG_NAME, 'tr')[0].find_elements(By.TAG_NAME, 'td')[1].text.split('\n')[0]
            cpf_polo_ativo = 'Não consta'
            try:
                adv_polo_ativo = table_partes.find_elements(By.TAG_NAME, 'tr')[0].find_elements(By.TAG_NAME, 'td')[1].text.split(':')[1].replace('Advogada','').replace('Advogado','')
            except Exception as e:
                adv_polo_ativo = 'Não consta'
            polo_passivo = table_partes.find_elements(By.TAG_NAME, 'tr')[1].find_elements(By.TAG_NAME, 'td')[1].text.split('\n')[0]
            cpf_polo_passivo = 'Não consta'
            
            try:
                adv_polo_passivo = table_partes.find_elements(By.TAG_NAME, 'tr')[1].find_elements(By.TAG_NAME, 'td')[1].text.split(':')[1].replace('Advogada','').replace('Advogado','')
            except:
                adv_polo_passivo = 'Não consta'
            processo_data = [self.bot_data.get('NUMERO_PROCESSO'), situaçãoproc, seção, julgador, relator, polo_ativo, adv_polo_ativo, polo_passivo, adv_polo_passivo]
            try:
                self.append_success(processo_data)
            except:
                pass
            
        return processo_data
