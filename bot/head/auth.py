import os
import string
import pathlib
import platform
import subprocess
from tqdm import tqdm
from time import sleep
from typing import Type
from contextlib import suppress

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException

if platform.system() == "Windows":
    from pywinauto.application import WindowSpecification
    from pywinauto import Application
    
from bot.head.Tools.PrintLogs import printtext as prt


class AuthBot:
    
    def __init__(self, elements, prt: Type[prt], 
                 driver: WebDriver, wait: WebDriverWait, 
                 info_creds: list, pid:str, method: str =  None, bot: str = None):
        
        self.driver  = driver
        self.wait = wait
        self.info_creds = info_creds
        self.method = method
        self.bot = bot
        self.pid = pid
        self.prt = prt
        self.elements = elements
        
    def set_portal(self) -> bool:
        
        metodo = getattr(self, self.bot)
        return metodo()
    
    def esaj(self):

            loginuser = ''.join(
                filter(lambda x: x not in string.punctuation, self.info_creds[0]))
            passuser = self.info_creds[1]
            sleep(3)

            if self.method == "cert":

                self.driver.get(self.elements.url_login)
                logincert: WebElement = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="certificados"]')))
                sleep(3)

                for cert in logincert:
                    loginopt = cert.find_elements(By.TAG_NAME, "option")

                    for option in loginopt:
                        if loginuser in option.text.lower():
                            try:
                                sencert = option.get_attribute("value")
                                select = Select(self.driver.find_element(
                                    By.CSS_SELECTOR, 'select[id="certificados"]'))
                                select.select_by_value(sencert)
                                entrar = self.driver.find_element(
                                    By.XPATH, '//*[@id="submitCertificado"]')
                                entrar.click()
                                sleep(2)

                                user_accept_cert_dir = os.path.join(
                                    os.getcwd(), "Browser", self.bot.split("_")[2], loginuser, "ACCEPTED")

                                user_data_dir = os.path.join(
                                    os.getcwd(), 'Temp', self.pid, 'chrome')

                                if not os.path.exists(user_accept_cert_dir):

                                    self.accept_cert(user_accept_cert_dir,
                                                user_data_dir)

                                break
                            except Exception as e:
                                return False
                
                checkloged = None
                with suppress(TimeoutException):
                
                    checkloged = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, '#esajConteudoHome > table:nth-child(4) > tbody > tr > td.esajCelulaDescricaoServicos')))
                    
                if not checkloged:
                    return False
                    
                return True


            self.driver.get(self.elements.url_login)

            userlogin = self.driver.find_element(By. CSS_SELECTOR, self.elements.campo_username)
            userlogin.click()
            userlogin.send_keys(loginuser)

            userpass = self.driver.find_element(By. CSS_SELECTOR, self.elements.campo_passwd)
            userpass.click()
            userpass.send_keys(passuser)
            entrar = self.driver.find_element(By.XPATH, self.elements.btn_entrar)
            entrar.click()
            sleep(2)

            checkloged = None
            with suppress(TimeoutException):
            
                checkloged = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '#esajConteudoHome > table:nth-child(4) > tbody > tr > td.esajCelulaDescricaoServicos')))
                
            if not checkloged:
                return False
                
            return True

    def projudi(self):
        
        if self.info_creds:
            
            # 0638164-88.2019.8.04.0015
            self.driver.get(self.elements.url_login)

            username: WebElement = self.wait.until(EC.presence_of_element_located ((By.CSS_SELECTOR, self.elements.campo_username)))
            username.send_keys(self.info_creds[0])

            password = self.driver.find_element(By.CSS_SELECTOR, self.elements.campo_passwd)
            password.send_keys(self.info_creds[1])

            entrar = self.driver.find_element(By.CSS_SELECTOR, self.elements.btn_entrar)
            entrar.click()
            
            check_login = None
            
            with suppress(TimeoutException):
                check_login = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[name="userMainFrame"]')))
            
            if check_login:
                return True
                
            return False
            
    def elaw(self):

        try:
            self.driver.get("https://amazonas.elaw.com.br/login")

            # wait until page load
            username: WebElement = self.wait.until(EC.presence_of_element_located((By.ID, 'username')))
            username.send_keys(self.info_creds[0])

            password: WebElement = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#password')))
            password.send_keys(self.info_creds[1])

            entrar: WebElement = self.wait.until(EC.presence_of_element_located((By.ID, "j_id_a_1_5_f")))
            entrar.click()

            sleep(7)
            
            url = self.driver.current_url
            
            if url == "https://amazonas.elaw.com.br/login":
                return False
            
            return True
        
        except Exception as e:
            return False

    def accept_cert(self, path_accepted, path_chrome):
        
        try:
            
            path = r"C:\Users\%USERNAME%\AppData\Local\Softplan Sistemas\Web Signer"
            resolved_path = os.path.expandvars(path)
            
            app = Application(backend="uia").connect(path=resolved_path, cache_enable=True)
            janela_principal = app.window()
            janela_principal.set_focus()
            button = janela_principal.descendants(control_type = "Button")
            checkbox = janela_principal.descendants(control_type = 'CheckBox')
            
            sleep(0.5)
            
            checkbox[0].click_input()
            sleep(0.5)
            button[1].click_input()
            
            target_directory = os.path.join(pathlib.Path(path_accepted).parent.resolve(), "chrome")
            
            os.makedirs(target_directory, exist_ok=True)
            
            source_directory = str(path_chrome)
            
            try:

                comando = ["xcopy", source_directory, target_directory, "/E", "/H", "/C", "/I"]

                resultados = subprocess.run(comando, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.splitlines()
                
                try:
                    print(resultados.stdout)
                    
                except:
                    pass
                
            except subprocess.CalledProcessError as e:
                tqdm.write(e.stderr)
                tqdm.write(e.stdout)
            
            with open(path_accepted.encode("utf-8"), "w") as f:
                f.write("")
        
        except Exception as e:
            print(e)

