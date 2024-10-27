from time import sleep
from contextlib import suppress
from bot.common.exceptions import ErroDeExecucao


from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from bot import CrawJUD


class SeachBot(CrawJUD):
    
    def __init__(self, Head: CrawJUD):
        
        self.__dict__ = Head.__dict__.copy()
        
    def __call__(self, Head: CrawJUD) -> None:
        
        self.__dict__ = Head.__dict__.copy()
        self.type_log = 'log'
        
        self.message = f'Buscando processos pelo nome "{self.parte_name}"'
        if self.typebot != "proc_parte":
            self.message = f'Buscando Processo Nº{self.bot_data.get("NUMERO_PROCESSO")}'
            
        self.prt(self)
        src: bool = getattr(self, f"{self.system.lower()}_search", None)()
        return src

    def elaw_search(self) -> bool:
        
        if self.driver.current_url != "https://amazonas.elaw.com.br/processoList.elaw":
        
            self.driver.get("https://amazonas.elaw.com.br/processoList.elaw")
        
        campo_numproc: WebElement = self.wait.until(EC.presence_of_element_located((By.ID, 'tabSearchTab:txtSearch')))
        campo_numproc.clear()
        sleep(0.15)
        self.interact.send_key(campo_numproc, self.bot_data.get("NUMERO_PROCESSO"))
        
        self.driver.find_element(By.ID, 'btnPesquisar').click()
        search_result: WebElement = self.wait.until(EC.presence_of_element_located((By.ID, 'dtProcessoResults_data')))
        
        open_proc = None
        with suppress(NoSuchElementException):
            open_proc = search_result.find_element(By.ID, 'dtProcessoResults:0:btnProcesso')

        sleep(1.5)
        
        if open_proc:
            chkTypeBot = not self.typebot.upper()\
                == "COMPLEMENT" and not self.typebot.upper() == "CADASTRO"
                
            if chkTypeBot:
                open_proc.click()
            
            return True
        
        return False
        
    def esaj_search(self) -> None:
        
        grau = int(self.bot_data.get("GRAU").replace("º", ""))
        if grau == 1:
            
            self.driver.get(self.elements.consultaproc_grau1)
            id_consultar = 'botaoConsultarProcessos'
            
        elif grau == 2:
            
            self.driver.get(self.elements.consultaproc_grau2)
            id_consultar = 'pbConsultar'
            
        elif not grau or grau != 1 or grau != 2:
            
            raise ErroDeExecucao("Informar instancia!")
        
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
            
    def projudi_search(self) -> None:

        self.driver.get(self.elements.url_busca)

        inputproc = None
        enterproc = None
        allowacess = None
        
        if self.typebot != "proc_parte":
            
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
                    self.type_log = "log"
                    self.prt(self)
                    
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
                        
                    return True
                
                elif not enterproc:
                    return False
            
        if self.typebot == "proc_parte":
            
            allprocess = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[value="qualquerAdvogado"]')))
            allprocess.click()
            
            data_inicio_formatted = self.data_inicio.strftime("%d/%m/%Y")
            data_fim_formatted = self.data_fim.strftime("%d/%m/%Y")
            
            if self.vara == 'TODAS AS COMARCAS':
                alljudge = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="pesquisarTodos"]')))
                alljudge.click()
                
            elif self.vara != 'TODAS AS COMARCAS':
                search_vara = self.driver.find_element(By.ID, 'descricaoVara')
                search_vara.click()
                search_vara.send_keys(self.vara)
                sleep(3)
                vara_option = self.driver.find_element(By.ID, 'ajaxAuto_descricaoVara').find_elements(By.TAG_NAME, 'li')[0]
                vara_option.click()
            
            sleep(3)
            input_parte = self.driver.find_element(By.CSS_SELECTOR, 'input[name="nomeParte"]')
            input_parte.send_keys(self.parte_name)
            
            cpfcnpj = self.driver.find_element(By.CSS_SELECTOR, 'input[name="cpfCnpj"]')
            cpfcnpj.send_keys(self.doc_parte)
            
            data_inicio = self.driver.find_element(By.CSS_SELECTOR, 'input[id="dataInicio"]')
            data_inicio.send_keys(data_inicio_formatted)
            
            data_fim = self.driver.find_element(By.CSS_SELECTOR, 'input[name="dataFim"]')
            data_fim.send_keys(data_fim_formatted)
            
            if self.polo_parte.lower() == 'reu':
                setréu = self.driver.find_element(By.CSS_SELECTOR, 'input[value="promovido"]')
                setréu.click()
                
            elif self.polo_parte.lower() == 'autor':
                setautor = self.driver.find_element(By. CSS_SELECTOR, 'input[value="promovente"')
                setautor.click()
            
            procenter = self.driver.find_element(By.ID, 'pesquisar')
            procenter.click()
            sleep(3)
                
            with suppress(TimeoutException):
                enterproc: WebElement = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'link')))
            
            if enterproc:
                return True
            
            return False
        
