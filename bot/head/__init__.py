""" Inicia """
from bot.head.auth import AuthBot
from bot.head.interator import Interact
from bot.head.nome_colunas import nomes_colunas
from bot.head.Tools.MakeTemplate import MakeXlsx
from bot.head.Tools.PrintLogs import printtext as prt
from bot.head.Tools.StartStop_Notify import SetStatus
from bot.head.Tools.dicionarios import cities_Amazonas

import os
import time
import glob
import json
import pytz
import pathlib
import openpyxl
import subprocess
import unicodedata
import pandas as pd
from tqdm import tqdm
from typing import Type
from datetime import datetime
from openpyxl.worksheet.worksheet import Worksheet
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

list_args = list_args = ['--ignore-ssl-errors=yes', '--ignore-certificate-errors',
                         "--display=:10", "--window-size=1600,900", "--no-sandbox", "--disable-blink-features=AutomationControlled",
                         '--kiosk-printing']
settings = {
    "recentDestinations": [{"id": "Save as PDF", "origin": "local", "account": ""}],
    "selectedDestinationId": "Save as PDF",
    "version": 2
}


class CrawJUD:

    def __init__(self):
        pass
    # def __init__(self, arguments_bot: dict):

    #     self.message = None
    #     self.arguments_bot = arguments_bot
    #     self.row = 2
    #     self.index = 0
    #     self.pid = arguments_bot["pid"]
    #     self.input_file = glob.glob(
    #         os.path.join("Temp", self.pid, "*.xlsx"))[0]
    #     self.ws: Type[Worksheet] = openpyxl.load_workbook(
    #         self.input_file).active
    #     self.output_dir_path = pathlib.Path(
    #         self.input_file).parent.resolve().__str__()
    #     self.prt = prt(self.pid)
    #     self.bot_name: str = arguments_bot.get("bot")
    #     args = self.DriverLaunch()
    #     self.senhacert = ""
    #     self.portal = ""
    #     self.bot = ""
    #     self.bot_data = {}
    #     self.set_status = SetStatus()

    #     if not args:
    #         self.prt.print_log('error', 'Erro ao inicializar Robô')
    #         status = [self.arguments_bot['user'], self.pid,
    #                   self.arguments_bot['bot'], 'Falha ao iniciar', self.input_file]
    #         self.set_status.botstop(status)
    #         return

    #     self.prt.print_log('log', 'Robô inicializado!')
    #     self.driver: Type[WebDriver] = args[0]
    #     self.wait: Type[WebDriverWait] = args[1]
    #     self.interact = Interact(self.driver, self.wait)
    #     status = [self.arguments_bot['user'], self.pid,
    #               self.arguments_bot['bot'], 'Em Execução', self.input_file]
    #     self.set_status.botstart(status)

    #     wb = openpyxl.load_workbook(filename=self.input_file)
    #     ws: Type[Worksheet] = wb.active
    #     self.rows = ws.max_row
    #     self.set_status.send_total_rows(self.rows, self.pid)
    #     self.login()
    #     self.prt.print_log('log', 'Criando planilha de output')
    #     namefile = f"Sucessos - PID {self.pid} {datetime.now(
    #         pytz.timezone('Etc/GMT+4')).strftime('%d-%m-%y')}.xlsx"
    #     self.path = f"{self.output_dir_path}/{namefile}"
    #     MakeXlsx().make_output(f"{self.bot_name}_sucesso", self.path)

    #     namefile_erro = f"Erros - PID {self.pid} {datetime.now(
    #         pytz.timezone('Etc/GMT+4')).strftime('%d-%m-%y')}.xlsx"
    #     self.path_erro = f"{self.output_dir_path}/{namefile_erro}"
    #     MakeXlsx().make_output(f"{self.bot_name}_erro", self.path_erro)

    #     self.prt.print_log('log', 'Planilha criada com sucesso!')

    def login(self):

        try:

            Get_Login = True
            upper_nome_bot = str(
                str(self.arguments_bot.get("bot")).split("_")[1]).upper()
            path_auth = os.path.join(os.getcwd(), 'Temp', self.pid, f'{
                                     self.arguments_bot.get("bot")}.json')
            self.portal = str(str(self.arguments_bot.get("bot")).split("_")[1])

            if os.path.exists(path_auth):

                self.bot = self.arguments_bot.get("bot")
                get_method = str(self.arguments_bot.get("bot")).split("_")
                method = ""
                if "esaj" == get_method[1] and "peticionamento" == get_method[-1]:
                    method = "cert"

                login: dict = json.load(open(path_auth))[
                    'login'][upper_nome_bot]
                self.prt.print_log('log', 'Usuário e senha obtidos!')
                auth = AuthBot(
                    prt=self.prt,
                    driver=self.driver, wait=self.wait,
                    info_creds=[login.get('username'), login['password']],
                    method=method, bot=self.bot, pid=self.pid)

                Get_Login = auth.set_portal(self.portal)

        except Exception as e:
            print(e)
            Get_Login = False

        if Get_Login is True:

            if os.path.exists(path_auth):
                self.senhacert = login.get("senha_token", "")
                self.prt.print_log('log', 'Login efetuado com sucesso!')

        elif Get_Login is False:

            self.driver.quit()
            self.prt.print_log('error', 'Erro ao realizar login')
            status = [self.arguments_bot['user'], self.pid,
                      self.arguments_bot['bot'], 'Falha ao iniciar', self.input_file]
            self.set_status.botstop(status)

    def set_data(self) -> dict:

        returns = {}
        for nome_coluna in nomes_colunas():
            nome_coluna = str(nome_coluna)
            nome_coluna_planilha = self.ws.cell(row=1, column=self.index).value
            valor_celula = self.ws.cell(row=self.row, column=self.index).value
            if nome_coluna_planilha and nome_coluna.upper() == str(nome_coluna_planilha).upper():
                if valor_celula:

                    if nome_coluna_planilha.upper() == "FASE":
                        pass

                    if isinstance(valor_celula, datetime):
                        valor_celula = str(valor_celula.strftime("%d/%m/%Y"))

                    elif str(nome_coluna_planilha).upper() == "DATA_LIMITE" and not self.bot_data.get("DATA_INICIO"):
                        self.bot_data.update({"DATA_INICIO": valor_celula})

                    elif isinstance(valor_celula, float):
                        valor_celula = "{:.2f}".format(
                            valor_celula).replace(".", ",")

                    elif isinstance(valor_celula, int):
                        valor_celula = str(valor_celula)

                    elif str(nome_coluna_planilha).upper() == "TIPO_EMPRESA":

                        self.bot_data.setdefault("TIPO_PARTE_CONTRARIA", "Réu")
                        if valor_celula == "Réu":
                            self.bot_data.update(
                                {"TIPO_PARTE_CONTRARIA": "Autor"})

                    elif str(nome_coluna_planilha).upper() == "COMARCA":
                        set_locale = cities_Amazonas().get(valor_celula, None)
                        if not set_locale:
                            set_locale = "Outro Estado"

                        self.bot_data.setdefault(
                            "CAPITAL_INTERIOR", set_locale)

                    returns = {nome_coluna.upper(): str(valor_celula)}
                    break

        return returns

    def calc_time(self) -> list:

        end_time = time.perf_counter()
        execution_time = end_time - self.start_time
        calc = execution_time/60
        splitcalc = str(calc).split(".")
        minutes = int(splitcalc[0])
        seconds = int(float(f"0.{splitcalc[1]}") * 60)

        return [minutes, seconds]

    def append_moves(self):

        if len(self.appends) > 0:
            self.append_success(
                self.appends, f'Movimentação salva na planilha com sucesso!!')

        else:
            raise ErroDeExecucao("Nenhuma Movimentação encontrada")

    def append_success(self, data: list, message: str = None):

        try:
            # Carrega a planilha existente
            existing_data = pd.read_excel(self.path)
        except FileNotFoundError:
            # Se a planilha não existir, cria uma nova
            existing_data = pd.DataFrame()
        # Converte a nova data em DataFrame e nomeia as colunas
        columns = existing_data.columns
        if isinstance(data[0], list):
            new_data = pd.DataFrame(data, columns=columns)
        else:
            new_data = pd.DataFrame([data], columns=columns)

        # Concatena os dados existentes com os novos dados
        updated_data = pd.concat(df.dropna(axis=1, how='all')
                                 for df in [existing_data, new_data])

        # Salva os dados atualizados de volta para a planilha
        updated_data.to_excel(self.path, index=False)

        if not message:
            message = f'Execução do processo Nº{data[0]} efetuada com sucesso!'

        self.prt.print_log('log', message)

    def append_error(self, motivo_erro: list):

        wb = openpyxl.load_workbook(filename=self.path_erro)
        sheet = wb.active

        sheet.append(motivo_erro)
        wb.save(self.path_erro)

    def format_String(self, string: str) -> str:

        return "".join([c for c in unicodedata.normalize('NFKD', string.lower().replace(" ", "").replace("_", "")) if not unicodedata.combining(c)])

    def finalize_execution(self):

        self.driver.delete_all_cookies()
        self.driver.quit()

        namefile = self.path.split("/")[-1]
        end_time = time.perf_counter()
        execution_time = end_time - self.start_time
        calc = execution_time / 60
        minutes = int(calc)
        seconds = int((calc - minutes) * 60)

        self.prt.print_log("log", f"Fim da execução, tempo: {
                           minutes} minutos e {seconds} segundos")

        status = [self.arguments_bot['user'], self.pid,
                  self.arguments_bot.get('bot'), 'Finalizado', namefile]
        self.set_status.botstop(status)

    def DriverLaunch(self) -> list | None:

        try:

            parent_path = os.path.join(os.getcwd())
            chrome_options = Options()
            user_data_dir = os.path.join(
                os.getcwd(), 'Temp', self.pid, 'chrome')

            if self.bot_name is not None and "esaj" in self.bot_name and "peticionamento" in self.bot_name:
                state = str(self.bot_name.split("_")[2])
                path_accepted = os.path.join(
                    parent_path, "Browser", state, self.arguments_bot['login'], "chrome")
                if os.path.exists(path_accepted):
                    try:
                        resultados = subprocess.run(["xcopy", path_accepted, user_data_dir, "/E", "/H", "/C", "/I"],
                                                    check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.splitlines()
                    except subprocess.CalledProcessError as e:
                        tqdm.write(e.stderr)
                        tqdm.write(e.stdout)

                else:
                    os.makedirs(os.path.join(
                        parent_path, "Browser"), exist_ok=True)
                    os.makedirs(os.path.join(
                        parent_path, "Browser", state), exist_ok=True)
                    os.makedirs(pathlib.Path(
                        path_accepted).parent.resolve(), exist_ok=True)

            chrome_options.add_argument(f"user-data-dir={user_data_dir}")
            for argument in list_args:
                chrome_options.add_argument(argument)

            for root, dirs, files in os.walk(os.path.join(os.getcwd())):
                for file in files:
                    if ".crx" in file:
                        path_plugin = os.path.join(root, file)
                        chrome_options.add_extension(path_plugin)
            chrome_prefs = {
                "download.prompt_for_download": False,
                "plugins.always_open_pdf_externally": True,
                "profile.default_content_settings.popups": 0,
                'printing.print_preview_sticky_settings.appState': json.dumps(settings),
                "download.default_directory": "{}".format(os.path.join(self.output_dir_path))
            }

            path_chrome = os.path.join(pathlib.Path(
                self.input_file).parent.resolve())
            driver_cache_manager = DriverCacheManager(root_dir=path_chrome)
            chrome_options.add_experimental_option("prefs", chrome_prefs)
            driverinst = ChromeDriverManager(
                cache_manager=driver_cache_manager).install()
            path = os.path.join(pathlib.Path(
                driverinst).parent.resolve(), "chromedriver.exe")
            driver = webdriver.Chrome(
                service=Service(path), options=chrome_options)

            wait = WebDriverWait(driver, 20, 0.01)
            args = [driver, wait]
            driver.delete_all_cookies()
            return args

        except Exception as e:

            print(e)
            if hasattr(e, 'msg') and e.msg is not None and e.msg != '':
                error_msg = e.msg.split(": ")[1]
                self.prt.print_log('error', f'System Error: {error_msg}')

            elif hasattr(e, 'args') and e.args is not None and e.args != '':
                error_msg = e.args[0]
                self.prt.print_log('error', f'System Error: {error_msg}')

            else:
                self.prt.print_log(self.pid, 'error',
                                   f'Não foi inicializar ChromeDriver')

            return None
