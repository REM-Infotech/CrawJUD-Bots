import os
import time
import shutil
import pathlib
import openpyxl
import unicodedata
from time import sleep
from typing import Type
from contextlib import suppress


""" Imports do Projeto """


from bot.head.common.exceptions import ErroDeExecucao


# Selenium Imports
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import  NoSuchElementException, TimeoutException, StaleElementReferenceException

from bot.head import CrawJUD


class protocolo(CrawJUD):

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
        
        if not search is True:
            raise ErroDeExecucao("Processo não encontrado!")
        
        self.detect_intimacao()
        
        self.add_new_move()
        self.add_new_file()
        if self.bot_data.get("ANEXOS", None) is not None:
            self.more_files()
            
        self.set_file_principal()
        self.sign_files()
        self.finish_move()
        self.screenshot_sucesso()
    
    def detect_intimacao(self) -> None:
        
        if "intimacaoAdvogado.do" in self.driver.current_url:
            raise ErroDeExecucao("Processo com Intimação pendente de leitura!")
      
    def add_new_move(self) -> None:

        try:
            self.message = 'Inicializando peticionamento...'
            self.type_log = "log"
            self.prt(self)
            button_add_move = self.driver.find_element(By.ID, 'peticionarButton')
            button_add_move.click()
            

            alert = None
            with suppress(TimeoutException):
                alert: Type[Alert] = WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            
            if alert: 
                alert.accept() 

            self.prt.print_log("log", 'Informando tipo de protocolo...')
            input_tipo_move: WebElement = self.wait.until(EC.presence_of_element_located ((By.CSS_SELECTOR, 'input[name="descricaoTipoDocumento"]')))
            input_tipo_move.click()
            sleep(1)
            input_tipo_move.send_keys(self.bot_data.get("TIPO_PROTOCOLO"))

            sleep(1.5)
            
            input_move_option: WebElement = self.wait.until(EC.presence_of_element_located ((By.XPATH, '//div[@id="ajaxAuto_descricaoTipoDocumento"]/ul/li')))
            input_move_option.click()
            
        except Exception as e:
            raise ErroDeExecucao()
   
    def add_new_file(self) -> None:

        try:
            file = str(self.bot_data.get("PETICAO_PRINCIPAL"))
            self.message = "Inserindo Petição/Anexos..."
            self.type_log = "log"
            self.prt(self)
            button_new_file = self.driver.find_element(By.CSS_SELECTOR, 'input#editButton[value="Adicionar"]')
            button_new_file.click()
            
            sleep(2.5)
    
            self.driver.switch_to.frame(self.driver.find_element(By.CSS_SELECTOR, 'iframe[frameborder="0"][id]'))
            self.message = f"Enviando arquivo '{file}'"
            self.type_log = "log"
            self.prt(self)
            
            css_inptfile = 'input[id="conteudo"]'
            input_file_element:WebElement = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_inptfile)))
            
            file_to_upload = "".join([c for c in unicodedata.normalize('NFKD', file.replace(" ", "").replace("_","")) if not unicodedata.combining(c)])
            
            path_file = os.path.join(pathlib.Path(self.path_args).parent.resolve(), file_to_upload)
            
            input_file_element.send_keys(path_file)
            
            self.wait_progressbar()

            self.message = "Arquivo enviado com sucesso!"
            self.type_log = "log"
            self.prt(self)       

            sleep(1)
            type_file: WebElement = self.wait.until(EC.presence_of_element_located((By.ID, f'tipo0')))
            type_file.click()
            sleep(0.25)
            type_options = type_file.find_elements(By.TAG_NAME, 'option')
            for option in type_options:
                if option.text == self.bot_data.get("TIPO_ARQUIVO"):
                    option.click()
                    break
        
        except Exception as e:
            raise ErroDeExecucao()
        
    def set_file_principal(self) -> None:

        try:
            tablefiles : WebElement = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'resultTable')))
            checkfiles = tablefiles.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME,'tr')[0]
            radiobutton = checkfiles.find_elements(By.TAG_NAME, 'td')[0].find_element(By.CSS_SELECTOR, 'input[type="radio"]')
            radiobutton.click()

        except Exception as e:
            raise ErroDeExecucao()
        
    def more_files(self) -> None:

        try:
            sleep(0.5)
            
            anexos_list = [str(self.bot_data.get("ANEXOS"))]
            if "," in self.bot_data.get("ANEXOS"):
                anexos_list = self.bot_data.get("ANEXOS").__str__().split(",")
            
            for file in anexos_list:
                
                self.message = f"Enviando arquivo '{file}'"
                file_to_upload = "".join([c for c in unicodedata.normalize('NFKD', file.replace(" ", "").replace("_","")) if not unicodedata.combining(c)])
                self.type_log = "log"
                self.prt(self)
                input_file_element:WebElement = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="conteudo"]')))
                input_file_element.send_keys(f'{os.path.join(pathlib.Path(self.path_args).parent.resolve())}/{file_to_upload}')
                self.wait_progressbar()
                self.message = f"Arquivo '{file}' enviado com sucesso!"
                self.type_log = "log"
            self.prt(self)
            
            sleep(3)
            tablefiles : WebElement = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'resultTable')))
            checkfiles = tablefiles.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME,'tr')
            
            for pos, file in enumerate(checkfiles):
                numbertipo = pos
                sleep(0.75)
                try:
                    type_file = self.driver.find_element(By.ID, f'tipo{numbertipo}')
                    type_file.click()
                except Exception as e:
                    break
                sleep(0.25)
                type_options = type_file.find_elements(By.TAG_NAME, 'option')
                for option in type_options:
                    if str(option.text).lower() == str(self.bot_data.get("TIPO_ANEXOS")).lower():
                        option.click()
                        break
        
        except Exception as e:
            raise ErroDeExecucao()
        
    def sign_files(self) -> None:

        try:
            self.prt.print_log("log", 'Assinando arquivos...')
            password_input = self.driver.find_element(By.ID, 'senhaCertificado')
            password_input.click()
            senhatoken = f'{self.senhacert}'
            password_input.send_keys(senhatoken)

            sign_button = self.driver.find_element(By.CSS_SELECTOR, 'input[name="assinarButton"]')
            sign_button.click()

            check_password = ''
            with suppress(TimeoutException):
                check_password:WebElement = WebDriverWait(self.driver, 5, 0.01).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#errorMessages > div.box-content')))

            if check_password != '':    
                raise ErroDeExecucao("Senha Incorreta!")
            
            confirm_button = self.driver.find_element(By.CSS_SELECTOR, 'input#closeButton[value="Confirmar Inclusão"]')
            confirm_button.click()
            sleep(1)

            self.driver.switch_to.default_content()
            self.prt.print_log("log", 'Arquivos assinados')
        
        except Exception as e:
            raise ErroDeExecucao()

    def finish_move(self) -> None:

        self.prt.print_log("log", f'Concluindo peticionamento do processo {self.bot_data.get("NUMERO_PROCESSO")}')
        finish_button = self.driver.find_element(By.CSS_SELECTOR, 'input#editButton[value="Concluir Movimento"]')
        finish_button.click()
        
    def screenshot_sucesso(self) -> None:
        
        try:
            sleep(2)

            filename = f'Protocolo - {self.bot_data.get("NUMERO_PROCESSO")} - PID{self.pid}.png'
            self.driver.get_screenshot_as_file(f"{self.output_dir_path}/{filename}")
            
            self.message = f'Peticionamento do processo Nº{self.bot_data.get("NUMERO_PROCESSO")} concluído com sucesso!'
            
            self.type_log = "log"
            self.prt(self)

            self.append_success([self.bot_data.get("NUMERO_PROCESSO"), self.message, filename])

            sleep(2)
            
        except Exception as e:
            raise ErroDeExecucao()

    def remove_files(self) -> None:
        
        tablefiles = None
        with suppress(TimeoutException):
            tablefiles : WebElement = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'resultTable')))

        if tablefiles:
        
            sleep(1)
            checkfiles = tablefiles.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME,'tr')
            
            for file in checkfiles:

                with suppress(NoSuchElementException, StaleElementReferenceException):
                    radiobutton = file.find_elements(By.TAG_NAME, 'td')[0].find_element(By.CSS_SELECTOR, 'input[type="radio"]')
                    radiobutton.click()
                    
                    delete_file = self.driver.find_element(By.CSS_SELECTOR, 'input[type="button"][name="deleteButton"]')
                    delete_file.click()
                    
                    alert = None
                    with suppress(TimeoutException):
                        alert: Type[Alert] = WebDriverWait(self.driver, 5).until(EC.alert_is_present())
                    
                    if alert: 
                        alert.accept()
                
                sleep(2)
            
    def wait_progressbar(self) -> None:
        
        while True:
            
            css_containerprogressbar = 'div[id="divProgressBarContainerAssinado"]'
            css_divprogressbar = 'div[id="divProgressBarAssinado"]'
            
            try:
                divprogressbar: WebElement = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_containerprogressbar)))
                divprogressbar = divprogressbar.find_element(By.CSS_SELECTOR, css_divprogressbar)
                sleep(1)
                try: # adicionar um suppress StaleElementReferenceException
                    get_style = divprogressbar.get_attribute("style")
                except:
                    break
                
                if get_style != '':
                    sleep(1)
                    
                elif get_style == '':
                    break
                
            except:
                break
            
            
            