import os
import time
import pytz
import json
import pathlib
import platform
import subprocess
import unicodedata
import pandas as pd
from typing import Union
from datetime import datetime
from pandas import Timestamp
from typing import Dict, List
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

# Selenium Imports
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from ..Utils.WebDriverManager import GetDriver

from ..common.exceptions import ErroDeExecucao

TypeHint = Union[
    List[str],
    List[Dict[str, str | int | float | datetime]],
    Dict[str, str],
]


class CrawJUD:

    def __init__(self, **kwrgs):
        self.__dict__.update(kwrgs)
        self.kwrgs = kwrgs
        self.setup()

    def __getattr__(self, nome: str) -> TypeHint:

        item = self.argbot.get(nome, None)

        if not item:
            item = self.__dict__.get(nome, None)

        return item

    settings = {
        "recentDestinations": [{"id": "Save as PDF", "origin": "local", "account": ""}],
        "selectedDestinationId": "Save as PDF",
        "version": 2,
    }

    row = 0
    message_error = None
    args_bot: dict[str, str | int] = {}
    bot_data: dict[str, str | int | datetime] = {}

    @property
    def AuthBot(self):
        from ..Utils.auth import AuthBot

        return AuthBot(**self.kwrgs)

    @property
    def SearchBot(self):
        from ..Utils.search import SeachBot

        return SeachBot

    @property
    def Interact(self):
        from ..Utils.interator import Interact

        return Interact

    @property
    def printtext(self):
        from ..Utils.PrintLogs import printtext

        return printtext

    @property
    def MakeXlsx(self):
        from ..Utils.MakeTemplate import MakeXlsx

        return MakeXlsx

    @property
    def cities_Amazonas(self):
        from ..Utils.dicionarios import cities_Amazonas

        return cities_Amazonas

    @property
    def elements(self):

        from ..Utils.elements import ElementsBot

        return ElementsBot

    @property
    def driver(self):
        return self.DriverLaunch()

    @property
    def wait(self):
        return self.wait

    @wait.setter
    def wait(self, wait: WebDriverWait):
        self.wait = wait

    def search(self):

        self.type_log = "log"

        self.message = f'Buscando processos pelo nome "{self.parte_name}"'
        if self.typebot != "proc_parte":
            self.message = f'Buscando Processo Nº{self.bot_data.get("NUMERO_PROCESSO")}'

        self.prt(self)
        result = self.SearchBot(**self.kwrgs)
        return result()

    def setup(self):

        self.prt = self.printtext(self)

        self.message = str("Inicializando robô")
        self.type_log = str("log")
        self.prt(self)

        self.graphicMode = "doughnut"
        with open(self.path_args, "rb") as f:
            json_f: dict[str, str | int] = json.load(f)

            self.argbot = json_f
            self.kwrgs.update(json_f)

            for key, value in json_f.items():
                setattr(self, key, value)

        self.output_dir_path = pathlib.Path(self.path_args).parent.resolve().__str__()
        # time.sleep(10)
        self.list_args = [
            "--ignore-ssl-errors=yes",
            "--ignore-certificate-errors",
            "--display=:99",
            "--window-size=1600,900",
            "--no-sandbox",
            "--disable-blink-features=AutomationControlled",
            "--kiosk-printing",
        ]

        if self.name_cert:

            self.install_cert()

        time_xlsx = datetime.now(pytz.timezone("America/Manaus")).strftime("%d-%m-%y")

        namefile = f"Sucessos - PID {self.pid} {time_xlsx}.xlsx"
        self.path = f"{self.output_dir_path}/{namefile}"

        namefile_erro = f"Erros - PID {self.pid} {time_xlsx}.xlsx"
        self.path_erro = f"{self.output_dir_path}/{namefile_erro}"

        self.name_colunas = self.MakeXlsx("sucesso", self.typebot).make_output(
            self.path
        )
        self.MakeXlsx("erro", self.typebot).make_output(self.path_erro)

        if not self.xlsx:

            self.data_inicio = datetime.strptime(self.data_inicio, "%Y-%m-%d")
            self.data_fim = datetime.strptime(self.data_fim, "%Y-%m-%d")

        cl = self.state
        if not cl:
            cl = self.client.split(" ")[0]

        self.elements(system_bot=self.system, state_or_client=cl)
        if self.login_method:
            chk_logged = self.AuthBot()
            if chk_logged is True:

                self.message = "Login efetuado com sucesso!"
                self.type_log = "log"
                self.prt(self)

            elif chk_logged is False:

                self.driver.quit()
                self.message = "Erro ao realizar login"
                self.type_log = "error"
                self.prt(self)
                raise Exception(self.message)

        # try:

        #     # Carrega elementos do bot
        #

        #

        #     args = self.DriverLaunch()
        #     if not args:

        #         self.message = "Erro ao inicializar WebDriver"
        #         self.type_log = "error"
        #         self.prt(self)
        #         return

        #     self.interact = self.Interact(self)

        #     if self.login_method:
        #         Get_Login = self.login()
        #         if Get_Login is True:

        #             self.message = "Login efetuado com sucesso!"
        #             self.type_log = "log"
        #             self.prt(self)

        #         elif Get_Login is False:

        #             self.driver.quit()

        #             self.message = "Erro ao realizar login"
        #             self.type_log = "error"
        #             self.prt(self)

        #             with app.app_context():
        #                 self.SetStatus(
        #                     status="Falha ao iniciar",
        #                     pid=self.pid,
        #                     system=self.system,
        #                     typebot=self.typebot,
        #                 ).botstop()

        #             return

        #     self.search = self.SeachBot(self)

        #     bot = getattr(self, self.system)(self.typebot, self)
        #     bot()

        # except Exception as e:

        #     print(e)
        #     if self.driver:
        #         self.driver.quit()

        #     with app.app_context():
        #         self.SetStatus(
        #             status="Falha ao iniciar",
        #             system=self.system,
        #             pid=self.pid,
        #             typebot=self.typebot,
        #         ).botstop()

        #     self.row = 0
        #     self.message = "Falha ao iniciar. Informe a mensagem de erro ao suporte"
        #     self.type_log = "error"
        #     self.prt(self)
        #     self.message_error = str(e)
        #     self.prt(self)
        #     return

    def dataFrame(self) -> list[dict[str, str]]:

        input_file = os.path.join(
            pathlib.Path(self.path_args).parent.resolve().__str__(), str(self.xlsx)
        )

        df = pd.read_excel(input_file)
        df.columns = df.columns.str.upper()

        for col in df.columns.to_list():
            df[col] = df[col].apply(
                lambda x: (
                    x.strftime("%d/%m/%Y")
                    if type(x) is datetime or type(x) is Timestamp
                    else x
                )
            )

        for col in df.select_dtypes(include=["float"]).columns.to_list():
            df[col] = df[col].apply(lambda x: "{:.2f}".format(x).replace(".", ","))

        vars_df = []

        df_dicted = df.to_dict(orient="records")
        for item in df_dicted:
            for key, value in item.items():
                if str(value) == "nan":
                    item.update({key: None})

            vars_df.append(item)

        return vars_df

    def elawFormats(self, data: dict[str, str]) -> dict[str, str]:

        data_listed = list(data.items())
        for key, value in data_listed:

            if key.upper() == "TIPO_EMPRESA":
                data.update({"TIPO_PARTE_CONTRARIA": "Autor"})
                if value.upper() == "RÉU":
                    data.update({"TIPO_PARTE_CONTRARIA": "Autor"})

            elif key.upper() == "COMARCA":
                set_locale = self.cities_Amazonas().get(value, None)
                if not set_locale:
                    set_locale = "Outro Estado"

                data.update({"CAPITAL_INTERIOR": set_locale})

            elif key == "DATA_LIMITE" and not data.get("DATA_INICIO"):
                data.update({"DATA_INICIO": value})

            elif type(value) is int or type(value) is float:
                data.update({key: "{:.2f}".format(value).replace(".", ",")})

            elif key == "CNPJ_FAVORECIDO" and not value:
                data.update({key: "04.812.509/0001-90"})

        return data

    def calc_time(self) -> list:

        end_time = time.perf_counter()
        execution_time = end_time - self.start_time
        calc = execution_time / 60
        splitcalc = str(calc).split(".")
        minutes = int(splitcalc[0])
        seconds = int(float(f"0.{splitcalc[1]}") * 60)

        return [minutes, seconds]

    def append_moves(self) -> None:

        if len(self.appends) > 0:
            self.append_success(
                self.appends, "Movimentação salva na planilha com sucesso!!"
            )

        elif len(self.appends) == 0:
            raise ErroDeExecucao("Nenhuma Movimentação encontrada")

    def append_success(
        self,
        data: list[dict[str, str]] = None,
        message="Execução do processo efetuada com sucesso!",
        fileN: str = None,
    ):

        def save_info(data: list[dict[str, str]]):
            if not self.path:
                self.path = os.path.join(
                    pathlib.Path(self.path).parent.resolve(), fileN
                )

            if not os.path.exists(self.path):
                df = pd.DataFrame(data)
                df = df.to_dict(orient="records")

            elif os.path.exists(self.path):

                df = pd.read_excel(self.path)
                df = df.to_dict(orient="records")
                df.extend(data)

            new_data = pd.DataFrame(df)
            new_data.to_excel(self.path, index=False)

        typeD = type(data) is list and all(isinstance(item, dict) for item in data)

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

        return "".join(
            [
                c
                for c in unicodedata.normalize("NFKD", string.upper())
                if not unicodedata.combining(c)
            ]
        )

    def finalize_execution(self) -> None:

        self.driver.delete_all_cookies()
        self.driver.close()

        end_time = time.perf_counter()
        execution_time = end_time - self.start_time
        calc = execution_time / 60
        minutes = int(calc)
        seconds = int((calc - minutes) * 60)

        with self.app.app_context():
            self.SetStatus(
                status="Finalizado",
                pid=self.pid,
                system=self.system,
                typebot=self.typebot,
            ).botstop()

        self.type_log = "success"
        self.message = f"Fim da execução, tempo: {minutes} minutos e {seconds} segundos"
        self.prt(self)

    def DriverLaunch(self) -> WebDriver:

        try:
            self.message = "Inicializando WebDriver"
            self.type_log = "log"
            self.prt(self)

            chrome_options = Options()
            self.user_data_dir = str(
                os.path.join(os.getcwd(), "Temp", self.pid, "chrome")
            )

            if not os.getlogin() == "root" or platform.system() != "Linux":
                self.list_args.remove("--no-sandbox")

            if platform.system() == "Windows" and self.login_method == "cert":
                state = str(self.state)
                self.path_accepted = str(
                    os.path.join(os.getcwd(), "Browser", state, self.login, "chrome")
                )
                path_exist = os.path.exists(self.path_accepted)
                if path_exist:
                    try:
                        resultados = subprocess.run(
                            [
                                "xcopy",
                                self.path_accepted,
                                self.user_data_dir,
                                "/E",
                                "/H",
                                "/C",
                                "/I",
                            ],
                            check=True,
                            text=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                        ).stdout.splitlines()

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
                "printing.print_preview_sticky_settings.appState": json.dumps(
                    self.settings
                ),
                "download.default_directory": "{}".format(
                    os.path.join(self.output_dir_path)
                ),
            }

            chrome_options.add_experimental_option("prefs", chrome_prefs)
            pid_path = pathlib.Path(self.path_args).parent.resolve()
            getdriver = GetDriver(destination=pid_path)
            path_chrome = os.path.join(pid_path, getdriver())

            driver = webdriver.Chrome(
                service=Service(path_chrome), options=chrome_options
            )
            wait = WebDriverWait(driver, 20, 0.01)
            driver.delete_all_cookies()

            self.wait = wait

            self.message = "WebDriver inicializado"
            self.type_log = "log"
            self.prt(self)

            return driver

        except Exception as e:
            raise e

    def install_cert(self) -> None:

        path_cert = str(os.path.join(self.output_dir_path, self.name_cert))
        comando = [
            "certutil",
            "-importpfx",
            "-user",
            "-f",
            "-p",
            self.password,
            "-silent",
            path_cert,
        ]
        try:
            # Quando você passa uma lista, você geralmente não deve usar shell=True
            resultado = subprocess.run(
                comando,
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

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

    def Select2_ELAW(self, elementSelect: str, to_Search: str):

        selector: WebElement = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, elementSelect))
        )

        items = selector.find_elements(By.TAG_NAME, "option")
        opt_itens: dict[str, str] = {}

        elementsSelecting = elementSelect.replace("'", "'")
        if '"' in elementsSelecting:
            elementsSelecting = elementSelect.replace('"', "'")

        for item in items:

            value_item = item.get_attribute("value")
            cms = f"{elementsSelecting} > option[value='{value_item}']"
            text_item = self.driver.execute_script(f'return $("{cms}").text();')

            opt_itens.update({text_item.upper(): value_item})

        value_opt = opt_itens.get(to_Search.upper())

        if value_opt:

            command = f"$('{elementSelect}').val(['{value_opt}']);"
            command2 = f"$('{elementSelect}').trigger('change');"

            if "'" in elementSelect:
                command = f"$(\"{elementSelect}\").val(['{value_opt}']);"
                command2 = f"$(\"{elementSelect}\").trigger('change');"

            self.driver.execute_script(command)
            self.driver.execute_script(command2)
