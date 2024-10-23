""" Inicia """
from flask import Flask

import os
import time
import pytz
import json
import pathlib
import openpyxl
import platform
import subprocess
import unicodedata
import pandas as pd
from pandas import Timestamp
from typing import Type, Union, Callable
from datetime import datetime
# from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.workbook.workbook import Workbook
from webdriver_manager.chrome import ChromeDriverManager

# Selenium Imports
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.core.driver_cache import DriverCacheManager
from bot.head.common.exceptions import ErroDeExecucao
from initbot import WorkerThread



class CrawJUD(WorkerThread):

    settings = {
        "recentDestinations": [{"id": "Save as PDF", "origin": "local", "account": ""}],
        "selectedDestinationId": "Save as PDF",
        "version": 2
    }


    def __init__(self, worker_thread: WorkerThread):
            
        self.__dict__ = worker_thread.__dict__.copy()
        self.prt: Type[printtext] = printtext(self)
    
    def __getattr__(self, nome_do_atributo: str) -> Union[
        Callable[[], None], list[dict[str, str]], list[str], 
        str, int, datetime]:
        item = getattr(self.argbot, nome_do_atributo, None) 
        return item
    
    
    def setup(self, app: Flask, path_args: str = None):
        
        self.driver = None
        with open(path_args, "rb") as f:
            json_f: dict[str, str | int] = json.load(f)
            
            setattr(self, "argbot", json_f)
            
            for key, value in json_f.items():
                setattr(self, key, value)
        
        time.sleep(10)
        self.list_args = ['--ignore-ssl-errors=yes', '--ignore-certificate-errors', "--display=:99", "--window-size=1600,900", 
                 "--no-sandbox", "--disable-blink-features=AutomationControlled", '--kiosk-printing']    

        ## Definição de variaveis utilizadas pelos robôs
        self.row = int(0)
        self.app = app
        self.message_error = None
        self.message = str('Inicializando robô')
        self.type_log = str("log")
        self.prt(self)
        
        self.output_dir_path = pathlib.Path(path_args).parent.resolve().__str__()
        self.bot_data: dict[str, str | int | datetime] = {}
        
        if self.name_cert:
            
            self.install_cert()
        
        ## Abertura da planilha de input
        self.path_args = path_args
        ## Criação das planilhas de output
        time_xlsx = datetime.now(pytz.timezone('Etc/GMT+4')).strftime('%d-%m-%y')
        
        namefile = f"Sucessos - PID {self.pid} {time_xlsx}.xlsx"
        self.path = f"{self.output_dir_path}/{namefile}"

        namefile_erro = f"Erros - PID {self.pid} {time_xlsx}.xlsx"
        self.path_erro = f"{self.output_dir_path}/{namefile_erro}"
        
        self.name_colunas = MakeXlsx("sucesso", self.typebot).make_output(self.path)
        MakeXlsx("erro", self.typebot).make_output(self.path_erro)
        
        if not self.xlsx:
            
            self.data_inicio = datetime.strptime(self.data_inicio, "%Y-%m-%d")
            self.data_fim = datetime.strptime(self.data_fim, "%Y-%m-%d")
            
        try:
            
            ## Carrega elementos do bot
            cl = self.state
            if not cl:
                cl = self.client.split(" ")[0]
            
            self.elements = elements_bot(self.system, cl)
            
            args = self.DriverLaunch()
            if not args:
                
                self.message = "Erro ao inicializar WebDriver"
                self.type_log = "error"
                self.prt(self)
                return

            self.interact = Interact(self)
            
            Get_Login = self.login()
            if Get_Login is True:
                
                self.message = 'Login efetuado com sucesso!'
                self.type_log = "log"
                self.prt(self)

            elif Get_Login is False:

                self.driver.quit()
                
                self.message = 'Erro ao realizar login'
                self.type_log = "error"
                self.prt(self)
                
                with app.app_context():
                    SetStatus(status='Falha ao iniciar', pid=self.pid, 
                            system=self.system, typebot=self.typebot).botstop()
                
                return

            self.search = SeachBot(self)
            
            bot = master_bots(self.system, self.typebot, self)
            bot()
            
        except Exception as e:
            
            print(e)
            if self.driver:
                self.driver.quit()
            
            with app.app_context():
                SetStatus(status='Falha ao iniciar', pid=self.pid, 
                        system=self.system, typebot=self.typebot).botstop()

            self.row = 0
            self.message = f'Falha ao iniciar. Informe a mensagem de erro ao suporte'
            self.type_log = "error"
            self.prt(self)
            self.message_error = str(e)
            self.prt(self)
            return

    def login(self) -> None:

        try:

            Get_Login = True
            if self.login:
                
                self.message = 'Usuário e senha obtidos!'
                self.type_log = "log"
                self.prt(self)
                
                self.auth = AuthBot(self)
                Get_Login = self.auth(self)

        except Exception as e:
            print(e)
            Get_Login = False

        return Get_Login
    
    def dataFrame(self) -> list[dict[str, str]]:

        input_file = os.path.join(pathlib.Path(
            self.path_args).parent.resolve().__str__(), str(self.xlsx))
        
        df = pd.read_excel(input_file)
        df.columns = df.columns.str.upper()
        
        for col in df.columns.to_list():
            df[col] = df[col].apply(lambda x: x.strftime('%d/%m/%Y') if type(x)\
                == datetime or type(x) == Timestamp else x)
            
        for col in df.select_dtypes(include=["float"]).columns.to_list():
            df[col] = df[col].apply(lambda x: "{:.2f}".format(x).replace(".", ","))
            
        return df.to_dict(orient="records")
    
    def elawFormats(self, data: dict[str, str]) -> dict[str, str]:
        
        data_listed = list(data.items())
        for key, value in data_listed:
            
            if key.upper() == "TIPO_EMPRESA":
                data.update({"TIPO_PARTE_CONTRARIA": "Autor"})
                if value.upper() == "RÉU":
                    data.update({"TIPO_PARTE_CONTRARIA": "Autor"})
                    
            elif key.upper() == "COMARCA":
                set_locale = cities_Amazonas().get(value, None)
                if not set_locale:
                    set_locale = "Outro Estado"

                data.update({"CAPITAL_INTERIOR": set_locale})
                
            elif key == "DATA_LIMITE" and not data.get("DATA_INICIO"):
                data.update({"DATA_INICIO": value})   
                
            
        return data

    def calc_time(self) -> list:

        end_time = time.perf_counter()
        execution_time = end_time - self.start_time
        calc = execution_time/60
        splitcalc = str(calc).split(".")
        minutes = int(splitcalc[0])
        seconds = int(float(f"0.{splitcalc[1]}") * 60)

        return [minutes, seconds]

    def append_moves(self) -> None:

        if len(self.appends) > 0:
            self.append_success(
                self.appends, f'Movimentação salva na planilha com sucesso!!')

        elif len(self.appends) == 0:
            raise ErroDeExecucao("Nenhuma Movimentação encontrada")

    def append_success(self, data: list[dict[str, str]] = None,
                        message: str = None, fileN: str = None,):
        
        def save_info(data: list[dict[str, str]]):
            if not self.path:
                self.path = os.path.join(pathlib.Path(self.path).parent.resolve(), fileN)
                
            if not os.path.exists(self.path):
                df = pd.DataFrame(data)
                df = df.to_dict(orient="records")
                
                
            elif os.path.exists(self.path):
                
                df = pd.read_excel(self.path)
                df = df.to_dict(orient="records")
                df.extend(data)   
            
            new_data = pd.DataFrame(df)
            new_data.to_excel(self.path, index=False)
        
        typeD = (type(data) == list
            and
            all(isinstance(item, dict) for item in data))
        
        if not typeD:
            
            data2 = {}
            
            for item in self.name_colunas:
                data2.update({item: ""})
            
            for item in data:    
                for key, value in list(data2.items()):
                    if not value:
                        data2.update({key: item})
                        break
                    
            data.clear()
            data.append(data2)

        save_info(data)                

        if not message:
            message = f'Execução do processo efetuada com sucesso!'

        if message:
            if self.type_log == "log":
                self.type_log = "success"
                
            self.message = message
            self.prt(self)

    def append_error(self, data: dict[str, str] = None):
        
        if not os.path.exists(self.path_erro):
            df = pd.DataFrame(data)
            df = df.to_dict(orient="records")
            
        elif os.path.exists(self.path_erro):
            df = pd.read_excel(self.path_erro)
            df = df.to_dict(orient="records")
            df.extend([data])
        
        new_data = pd.DataFrame(df)
        new_data.to_excel(self.path_erro, index=False)

    def format_String(self, string: str) -> str:

        return "".join([c for c in unicodedata.normalize('NFKD', string.lower().replace(" ", "").replace("_", "")) if not unicodedata.combining(c)])

    def finalize_execution(self) -> None:

        self.row += 1
        self.driver.delete_all_cookies()
        self.driver.close()

        end_time = time.perf_counter()
        execution_time = end_time - self.start_time
        calc = execution_time / 60
        minutes = int(calc)
        seconds = int((calc - minutes) * 60)
        
        with self.app.app_context():
            SetStatus(status='Finalizado', pid=self.pid, 
                    system=self.system, typebot=self.typebot).botstop()
            
        self.type_log = "success"
        self.message = f"Fim da execução, tempo: {minutes} minutos e {seconds} segundos"
        self.prt(self)

    def DriverLaunch(self) -> bool:
        
        try:
            self.message = 'Inicializando WebDriver'
            self.type_log = "log"
            self.prt(self)
            
            chrome_options = Options()
            self.user_data_dir = str(os.path.join(os.getcwd(), 'Temp', self.pid, 'chrome'))
            
            if not os.getlogin() == "root" or platform.system() != "Linux":
                self.list_args.remove("--no-sandbox")
            
            if platform.system() == "Windows" and self.login_method == "cert":
                state = str(self.state)
                self.path_accepted = str(os.path.join(os.getcwd(), "Browser", state, self.argbot['login'], "chrome"))
                path_exist =  os.path.exists(self.path_accepted)
                if path_exist:
                    try:
                        resultados = subprocess.run(["xcopy", self.path_accepted, self.user_data_dir, "/E", "/H", "/C", "/I"],
                        check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.splitlines()
                        
                        for item in resultados:
                            print(item)
                        
                    except subprocess.CalledProcessError as e:
                        raise e

                elif not path_exist:
                    os.makedirs(self.path_accepted, exist_ok=True)

            chrome_options.add_argument(f"user-data-dir={self.user_data_dir}")
            for argument in self.list_args:
                chrome_options.add_argument(argument)

            this_path = pathlib.Path(__file__).parent.resolve().__str__()
            path_extensions = os.path.join(this_path, "extensions")
            for root, dirs, files in os.walk(path_extensions):
                for file_ in files:
                    if ".crx" in file_:
                        path_plugin = os.path.join(root, file_)
                        chrome_options.add_extension(path_plugin)
            chrome_prefs = {
                "download.prompt_for_download": False,
                "plugins.always_open_pdf_externally": True,
                "profile.default_content_settings.popups": 0,
                'printing.print_preview_sticky_settings.appState': json.dumps(self.settings),
                "download.default_directory": "{}".format(os.path.join(self.output_dir_path))
            }
            
            path_chrome = os.path.join(pathlib.Path(self.path_args).parent.resolve())
            driver_cache_manager = DriverCacheManager(root_dir=path_chrome)
            chrome_options.add_experimental_option("prefs", chrome_prefs)
            driverinst = ChromeDriverManager(cache_manager=driver_cache_manager).install()
            
            driverinst = pathlib.Path(driverinst).parent.resolve().__str__()
            path = os.path.join(driverinst, "chromedriver.exe")
            
            if platform.system() != "Windows":
                path = path.replace(".exe", "")
            
            driver = webdriver.Chrome(service=Service(path), options=chrome_options)
            wait = WebDriverWait(driver, 20, 0.01)
            driver.delete_all_cookies()
            
            self.driver = driver
            self.wait = wait
            
            self.message = "WebDriver inicializado"
            self.type_log = "log"
            self.prt(self)
            
            return True

        except Exception as e:
            raise e

    def install_cert(self) -> None:

        path_cert = str(os.path.join(self.output_dir_path, self.name_cert))
        comando = ["certutil", "-importpfx", "-user", "-f", "-p", self.senhacert, "-silent", path_cert]
        try:
            # Quando você passa uma lista, você geralmente não deve usar shell=True
            resultado = subprocess.run(comando, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.message = str(resultado.stdout)
            self.type_log = str("log")
            self.prt(self)
            
        except subprocess.CalledProcessError as e:
            raise e

    def group_date_all(self, data: dict[str, dict[str, str]]) -> list[dict[str, str]]:

        
        records = []
        for vara, dates in data.items():
            record = {}
            for date, entries in dates.items():
                for entry in entries:
                    
                    record.update({"Data": date, "Vara": vara})
                    record.update(entry)
                    records.append(record)

        return records

    def group_keys(self, data: list[dict[str, str]]) -> dict[str, str]:

        record = {}
        for pos, entry in enumerate(data):
            for key, value in entry.items():
                    
                if not record.get(key):   
                    record.update({key: {}})
                    
                record.get(key).update({str(pos): value})
        return record

from bot.pje import pje, elements_pje
from bot.esaj import esaj, elements_esaj
from bot.elaw import elaw, elements_elaw
from bot.caixa import caixa, elements_caixa
from bot.projudi import projudi, elements_projudi

def master_bots(system: str, type_bot: str, master: CrawJUD) -> Callable[[], str]:
    
    call_act: Callable[[], None] | None = globals().get(system.lower())
    
    if call_act:
        call_act = call_act(type_bot, master)
    
    return call_act
        
def elements_bot(system: str, state: str) -> Callable[[], str]:
    
    call_act: Callable[
        [], None] | None = globals().get(f"elements_{system.lower()}")
    
    if call_act:
        call_act = call_act(state)()
    
    return call_act



from bot.head.auth import AuthBot
from bot.head.search import SeachBot
from bot.head.interator import Interact
from bot.head.nome_colunas import nomes_colunas
from bot.head.Tools.MakeTemplate import MakeXlsx
from bot.head.Tools.PrintLogs import printtext
from bot.head.Tools.dicionarios import cities_Amazonas
from bot.head.common.exceptions import ErroDeExecucao
from bot.head.Tools.StartStop_Notify import SetStatus