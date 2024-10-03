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

from bot.projudi.common.elements import elements_projudi
from bot.esaj.common.elements import elements_esaj

typings = elements_projudi | elements_esaj

class SeachBot:
    
    def __init__(self, elementos: Type[typings], driver: Type[WebDriver], wait: Type[WebDriverWait], portal, bot: str = None) -> None:
        
        self.elementos = elementos
        self.driver = driver
        self.wait = wait
        self.bot = bot
        
        self.interact = Interact(self.driver, self.wait)
        
        metodo = getattr(self, portal, None)
        self.metodo = metodo
        
    def search(self, bot_data: dict, prt: Type[prt]) -> None:
        
        self.bot_data = bot_data
        self.prt = prt
        
        self.prt.print_log('log', f'Buscando Processo Nº{self.bot_data.get("NUMERO_PROCESSO")}')
        return self.metodo()

    def elaw(self) -> bool:
        
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
        
    def esaj(self):
        
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
            
    def projudi(self):

        self.driver.get(self.elementos.url_busca)

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
