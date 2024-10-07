from time import sleep
from typing import Type
from contextlib import suppress
from bot.head.common.exceptions import ErroDeExecucao

from bot.head.Tools.PrintLogs import printtext as prt
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import  NoSuchElementException, TimeoutException
from bot.head.interator import Interact
from bot.head import CrawJUD

class SeachBot(CrawJUD):
    
    def __init__(self, Head: CrawJUD):
        
        self.__dict__ = Head.__dict__.copy()
        self.metodo = getattr(self, f"{self.system.lower()}_search", None)
        
    def __call__(self) -> None:
        
        self.type_log = 'log'
        self.message = f'Buscando Processo Nº{self.bot_data.get("NUMERO_PROCESSO")}'
        self.prt(self)()
        self.metodo()

    def elaw_search(self) -> bool:
        
        if self.driver.current_url != "https://amazonas.elaw.com.br/processoList.elaw":
        
            self.driver.get("https://amazonas.elaw.com.br/processoList.elaw")
        
        campo_numproc: WebElement = self.wait.until(EC.presence_of_element_located((By.ID,'tabSearchTab:txtSearch')))
        campo_numproc.clear()
        sleep(0.15)
        self.interact.send_key(campo_numproc, self.bot_data.get("NUMERO_PROCESSO"))
        
        self.driver.find_element(By.ID, 'btnPesquisar').click()
        search_result: WebElement = self.wait.until(EC.presence_of_element_located((By.ID,'dtProcessoResults_data')))
        
        open_proc = None
        with suppress(NoSuchElementException):
            open_proc = search_result.find_element(By.ID, 'dtProcessoResults:0:btnProcesso')

        sleep(1.5)
        
        if open_proc:
            
            if self.bot is None:
                open_proc.click()
            
            return True
        
        return False
        
    def esaj_search(self):
        
        grau = int(str(self.bot_data.get("GRAU")).replace("º", ""))
        if grau == 1:
            
            self.driver.get('https://consultasaj.tjam.jus.br/cpopg/open.do')
            id_consultar = 'botaoConsultarProcessos'
            
        elif grau == 2:

            self.driver.get('https://consultasaj.tjam.jus.br/cposgcr/')
            id_consultar = 'pbConsultar'
        
        sleep(1)
        ## Coloca o campo em formato "Outros" para inserir o número do processo
        ratioNumberOld: WebElement = self.wait.until(EC.presence_of_element_located((By.ID, 'radioNumeroAntigo')))
        self.interact.click(ratioNumberOld)

        ## Insere o processo no Campo
        lineprocess: WebElement = self.wait.until(EC.presence_of_element_located((By.ID, 'nuProcessoAntigoFormatado')))
        self.interact.click(lineprocess)
        self.interact.send_key(lineprocess, self.bot_data.get("NUMERO_PROCESSO"))


        ## Abre o Processo
        openprocess: WebElement = self.wait.until(EC.presence_of_element_located((By.ID, id_consultar)))
        self.interact.click(openprocess)
            
    def projudi_search(self):

        self.driver.get(self.elements.url_busca)

        inputproc = None
        enterproc = None
        allowacess = None
        
        with suppress(TimeoutException):
            inputproc: WebElement = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#numeroProcesso')))
            
        if inputproc:
            self.interact.send_key(inputproc, self.bot_data.get('NUMERO_PROCESSO'))
            consultar = self.driver.find_element(By.CSS_SELECTOR, '#pesquisar')
            self.interact.click(consultar)
            
            with suppress(TimeoutException):
                enterproc: WebElement = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'link')))
                
            
            if enterproc:
                enterproc.click()
                self.message = "Processo encontrado!"
                self.prt.print_log("log", self.message)
                
                with suppress(TimeoutException, NoSuchElementException):
                
                    allowacess = self.driver.find_element(
                        By.CSS_SELECTOR, '#habilitacaoProvisoriaButton')
                    
                if allowacess:    
                    allowacess.click()
                    sleep(1)

                    confirmterms = self.driver.find_element(By.CSS_SELECTOR, '#termoAceito')
                    confirmterms.click()
                    sleep(1)

                    save = self.driver.find_element(By. CSS_SELECTOR, '#saveButton')
                    save.click()
            else:
                raise ErroDeExecucao("Processo não encontrado!")
