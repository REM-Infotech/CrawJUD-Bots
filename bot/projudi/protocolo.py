import os
import time
import pathlib
from PIL import Image
from time import sleep
from typing import Type
from contextlib import suppress


""" Imports do Projeto """


from bot.common.exceptions import ErroDeExecucao


# Selenium Imports
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    StaleElementReferenceException,
)

from bot.CrawJUD import CrawJUD


class protocolo(CrawJUD):

    def __init__(self, **kwrgs) -> None:
        super().__init__(**kwrgs)
        super().auth_bot()
        self.start_time = time.perf_counter()

    def execution(self) -> None:

        frame = self.dataFrame()
        self.max_rows = len(frame)

        for pos, value in enumerate(frame):

            self.row = pos + 2
            self.bot_data = value
            if self.isStoped:
                break

            if self.driver.title.lower() == "a sessao expirou":
                self.auth(self)

            try:
                self.queue()

            except Exception as e:

                old_message = self.message
                message_error = str(e)

                self.type_log = "error"
                self.message_error = f"{message_error}. | Operação: {old_message}"
                self.prt()

                self.bot_data.update({"MOTIVO_ERRO": self.message_error})
                self.append_error(self.bot_data)

                self.message_error = None

        self.finalize_execution()

    def queue(self) -> None:

        search = self.search()

        if search is not True:
            raise ErroDeExecucao("Processo não encontrado!")

        self.add_new_move()

        if self.set_parte() is not True:
            raise ErroDeExecucao("Não foi possível selecionar parte")

        self.add_new_file()
        if self.bot_data.get("ANEXOS", None) is not None:
            self.more_files()

        self.set_file_principal()
        self.sign_files()
        self.finish_move()

        confirm_protocol = self.confirm_protocol()
        if not confirm_protocol:

            if self.set_parte() is not True:
                raise ErroDeExecucao("Nao foi possivel confirmar protocolo")

            self.finish_move()
            confirm_protocol = self.confirm_protocol()
            if not confirm_protocol:
                raise ErroDeExecucao("Nao foi possivel confirmar protocolo")

        data = self.screenshot_sucesso()
        data.append(confirm_protocol)
        self.append_success(data)

    def confirm_protocol(self) -> str | None:

        successMessage = None
        with suppress(TimeoutException):
            successMessage = (
                self.wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "#successMessages")
                    )
                )
                .text.split("Protocolo:")[1]
                .replace(" ", "")
            )

        return successMessage

    def set_parte(self) -> bool:

        # self.driver.switch_to.frame(self.driver.find_element(By.CSS_SELECTOR, 'iframe[name="userMainFrame"]'))
        self.message = "Selecionando parte"
        self.type_log = "log"
        self.prt()

        table_partes = self.driver.find_element(
            By.CSS_SELECTOR, "#juntarDocumentoForm > table:nth-child(28)"
        )
        table_partes = table_partes.find_element(By.TAG_NAME, "tbody").find_elements(
            By.TAG_NAME, "tr"
        )

        selected_parte = False

        for pos, item in enumerate(table_partes):

            td_partes = table_partes[pos + 1].find_element(By.TAG_NAME, "td")
            parte_peticao = self.bot_data.get("PARTE_PETICIONANTE").upper()
            chk_info = td_partes.text.upper() == parte_peticao
            if "\n" in td_partes.text:
                partes = td_partes.text.split("\n")
                for enum, parte in enumerate(partes):

                    if parte.upper() == self.bot_data.get("PARTE_PETICIONANTE").upper():

                        radio_item = item.find_element(
                            By.CSS_SELECTOR, "input[type='radio']"
                        )
                        id_radio = radio_item.get_attribute("id")

                        command = f'document.getElementById("{id_radio}").removeAttribute("disabled");'
                        self.driver.execute_script(command)

                        radio_item.click()
                        set_parte = td_partes.find_elements(By.TAG_NAME, "input")[enum]

                        self.id_part = set_parte.get_attribute("id")
                        cmd2 = (
                            f"return document.getElementById('{self.id_part}').checked"
                        )
                        return_cmd = self.driver.execute_script(cmd2)
                        if return_cmd is False:
                            set_parte.click()
                            cmd2 = f"return document.getElementById('{self.id_part}').checked"
                            return_cmd = self.driver.execute_script(cmd2)
                            if return_cmd is False:
                                raise ErroDeExecucao("Não é possivel selecionar parte")

                        selected_parte = True
                        break

            elif chk_info:

                radio_item = item.find_element(By.CSS_SELECTOR, "input[type='radio']")
                radio_item.click()

                set_parte = td_partes.find_element(By.TAG_NAME, "input")

                self.id_part = set_parte.get_attribute("id")
                cmd2 = f"return document.getElementById('{self.id_part}').checked"
                return_cmd = self.driver.execute_script(cmd2)
                if return_cmd is False:
                    set_parte.click()
                    cmd2 = f"return document.getElementById('{self.id_part}').checked"
                    return_cmd = self.driver.execute_script(cmd2)
                    if return_cmd is False:
                        raise ErroDeExecucao("Não é possivel selecionar parte")

                selected_parte = True
                break

            if selected_parte:
                break

        return selected_parte

    def add_new_move(self) -> None:

        try:
            self.message = "Inicializando peticionamento..."
            self.type_log = "log"
            self.prt()
            button_add_move = self.driver.find_element(By.ID, "peticionarButton")
            button_add_move.click()

            alert = None
            with suppress(TimeoutException):
                alert: Type[Alert] = WebDriverWait(self.driver, 5).until(
                    EC.alert_is_present()
                )

            if alert:
                alert.accept()

            self.message = "Informando tipo de protocolo..."
            self.type_log = "log"
            self.prt()
            input_tipo_move: WebElement = self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'input[name="descricaoTipoDocumento"]')
                )
            )
            input_tipo_move.click()
            sleep(1)
            input_tipo_move.send_keys(self.bot_data.get("TIPO_PROTOCOLO"))

            sleep(1.5)

            input_move_option: WebElement = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@id="ajaxAuto_descricaoTipoDocumento"]/ul/li')
                )
            )
            input_move_option.click()

        except Exception as e:
            raise ErroDeExecucao(e=e)

    def add_new_file(self) -> None:

        try:
            file = str(self.bot_data.get("PETICAO_PRINCIPAL"))
            self.message = "Inserindo Petição/Anexos..."
            self.type_log = "log"
            self.prt()
            button_new_file = self.driver.find_element(
                By.CSS_SELECTOR, 'input#editButton[value="Adicionar"]'
            )
            button_new_file.click()

            sleep(2.5)

            self.driver.switch_to.frame(
                self.driver.find_element(By.CSS_SELECTOR, 'iframe[frameborder="0"][id]')
            )
            self.message = f"Enviando arquivo '{file}'"
            self.type_log = "log"
            self.prt()

            css_inptfile = 'input[id="conteudo"]'
            input_file_element: WebElement = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_inptfile))
            )

            file_to_upload = self.format_String(file)

            path_file = os.path.join(
                pathlib.Path(self.path_args).parent.resolve(), file_to_upload
            )

            input_file_element.send_keys(path_file)

            self.wait_progressbar()

            self.message = "Arquivo enviado com sucesso!"
            self.type_log = "log"
            self.prt()

            sleep(1)
            type_file: WebElement = self.wait.until(
                EC.presence_of_element_located((By.ID, "tipo0"))
            )
            type_file.click()
            sleep(0.25)
            type_options = type_file.find_elements(By.TAG_NAME, "option")
            for option in type_options:
                if option.text == self.bot_data.get("TIPO_ARQUIVO"):
                    option.click()
                    break

        except Exception as e:
            raise ErroDeExecucao(e=e)

    def set_file_principal(self) -> None:

        try:
            tablefiles: WebElement = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "resultTable"))
            )
            checkfiles = tablefiles.find_element(By.TAG_NAME, "tbody").find_elements(
                By.TAG_NAME, "tr"
            )[0]
            radiobutton = checkfiles.find_elements(By.TAG_NAME, "td")[0].find_element(
                By.CSS_SELECTOR, 'input[type="radio"]'
            )
            radiobutton.click()

        except Exception as e:
            raise ErroDeExecucao(e=e)

    def more_files(self) -> None:

        try:
            sleep(0.5)

            anexos_list = [str(self.bot_data.get("ANEXOS"))]
            if "," in self.bot_data.get("ANEXOS"):
                anexos_list = self.bot_data.get("ANEXOS").__str__().split(",")

            for file in anexos_list:

                self.message = f"Enviando arquivo '{file}'"
                file_to_upload = self.format_String(file)
                self.type_log = "log"
                self.prt()
                input_file_element: WebElement = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="conteudo"]'))
                )
                input_file_element.send_keys(
                    f"{os.path.join(pathlib.Path(self.path_args).parent.resolve())}/{file_to_upload}"
                )
                self.wait_progressbar()
                self.message = f"Arquivo '{file}' enviado com sucesso!"
                self.type_log = "log"
            self.prt()

            sleep(3)
            tablefiles: WebElement = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "resultTable"))
            )
            checkfiles = tablefiles.find_element(By.TAG_NAME, "tbody").find_elements(
                By.TAG_NAME, "tr"
            )

            for pos, file in enumerate(checkfiles):
                numbertipo = pos
                sleep(0.75)
                try:
                    type_file = self.driver.find_element(By.ID, f"tipo{numbertipo}")
                    type_file.click()
                except Exception:
                    break
                sleep(0.25)
                type_options = type_file.find_elements(By.TAG_NAME, "option")
                type_anexos = str(self.bot_data.get("TIPO_ANEXOS")).lower()
                for option in type_options:
                    if str(option.text).lower() == type_anexos:
                        option.click()
                        break

        except Exception as e:
            raise ErroDeExecucao(e=e)

    def sign_files(self) -> None:

        try:
            self.message = "Assinando arquivos..."
            self.type_log = "log"
            self.prt()
            password_input = self.driver.find_element(By.ID, "senhaCertificado")
            password_input.click()
            senhatoken = f"{self.token}"
            password_input.send_keys(senhatoken)

            sign_button = self.driver.find_element(
                By.CSS_SELECTOR, 'input[name="assinarButton"]'
            )
            sign_button.click()

            check_password = ""
            with suppress(TimeoutException):
                check_password: WebElement = WebDriverWait(self.driver, 5, 0.01).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "#errorMessages > div.box-content")
                    )
                )

            if check_password != "":
                raise ErroDeExecucao("Senha Incorreta!")

            confirm_button = self.driver.find_element(
                By.CSS_SELECTOR, 'input#closeButton[value="Confirmar Inclusão"]'
            )
            confirm_button.click()
            sleep(1)

            self.driver.switch_to.default_content()
            self.message = "Arquivos assinados"
            self.type_log = "log"
            self.prt()

        except Exception as e:
            raise ErroDeExecucao(e=e)

    def finish_move(self) -> None:

        self.message = f'Concluindo peticionamento do processo {self.bot_data.get("NUMERO_PROCESSO")}'
        self.type_log = "log"
        self.prt()

        cmd2 = f"return document.getElementById('{self.id_part}').checked"
        return_cmd = self.driver.execute_script(cmd2)
        if return_cmd is False:
            self.driver.find_element(By.ID, self.id_part).click()

        finish_button = self.driver.find_element(
            By.CSS_SELECTOR, 'input#editButton[value="Concluir Movimento"]'
        )
        finish_button.click()

    def screenshot_sucesso(self) -> None:

        try:

            table_moves = self.driver.find_element(By.CLASS_NAME, "resultTable")
            table_moves = table_moves.find_elements(
                By.XPATH,
                './/tr[contains(@class, "odd") or contains(@class, "even")][not(@style="display:none;")]',
            )

            table_moves[0].screenshot(os.path.join(self.output_dir_path, "tr_0.png"))

            expand = table_moves[0].find_element(
                By.CSS_SELECTOR, 'a[href="javascript://nop/"]'
            )
            expand.click()

            sleep(1.5)

            table_moves[1].screenshot(os.path.join(self.output_dir_path, "tr_1.png"))

            # Abra as imagens
            im_tr1 = Image.open(os.path.join(self.output_dir_path, "tr_0.png"))
            im_tr2 = Image.open(os.path.join(self.output_dir_path, "tr_1.png"))

            # Obtenha as dimensões das imagens
            width1, height1 = im_tr1.size
            width2, height2 = im_tr2.size

            # Calcule a largura e altura total para combinar as imagens
            total_height = height1 + height2
            total_width = max(width1, width2)

            # Crie uma nova imagem com o tamanho combinado
            combined_image = Image.new("RGB", (total_width, total_height))

            # Cole as duas imagens (uma em cima da outra)
            combined_image.paste(im_tr1, (0, 0))
            combined_image.paste(im_tr2, (0, height1))

            # Salve a imagem combinada
            comprovante1 = f'{self.pid} - COMPROVANTE 1 - {self.bot_data.get("NUMERO_PROCESSO")}.png'
            combined_image.save(os.path.join(self.output_dir_path, comprovante1))

            filename = f'Protocolo - {self.bot_data.get("NUMERO_PROCESSO")} - PID{self.pid}.png'
            self.driver.get_screenshot_as_file(
                os.path.join(self.output_dir_path, filename)
            )

            self.message = f'Peticionamento do processo Nº{self.bot_data.get("NUMERO_PROCESSO")} concluído com sucesso!'

            self.type_log = "log"
            self.prt()

            return [self.bot_data.get("NUMERO_PROCESSO"), self.message, comprovante1]

        except Exception as e:
            raise ErroDeExecucao(e=e)

    def remove_files(self) -> None:

        tablefiles = None
        with suppress(TimeoutException):
            tablefiles: WebElement = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "resultTable"))
            )

        if tablefiles:

            sleep(1)
            checkfiles = tablefiles.find_element(By.TAG_NAME, "tbody").find_elements(
                By.TAG_NAME, "tr"
            )

            for file in checkfiles:

                with suppress(NoSuchElementException, StaleElementReferenceException):
                    radiobutton = file.find_elements(By.TAG_NAME, "td")[0].find_element(
                        By.CSS_SELECTOR, 'input[type="radio"]'
                    )
                    radiobutton.click()

                    delete_file = self.driver.find_element(
                        By.CSS_SELECTOR, 'input[type="button"][name="deleteButton"]'
                    )
                    delete_file.click()

                    alert = None
                    with suppress(TimeoutException):
                        alert: Type[Alert] = WebDriverWait(self.driver, 5).until(
                            EC.alert_is_present()
                        )

                    if alert:
                        alert.accept()

                sleep(2)

    def wait_progressbar(self) -> None:

        while True:

            css_containerprogressbar = 'div[id="divProgressBarContainerAssinado"]'
            css_divprogressbar = 'div[id="divProgressBarAssinado"]'

            try:
                divprogressbar: WebElement = self.wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, css_containerprogressbar)
                    )
                )
                divprogressbar = divprogressbar.find_element(
                    By.CSS_SELECTOR, css_divprogressbar
                )
                sleep(1)
                try:
                    # adicionar um suppress StaleElementReferenceException
                    get_style = divprogressbar.get_attribute("style")
                except Exception:
                    break

                if get_style != "":
                    sleep(1)

                elif get_style == "":
                    break

            except Exception:
                break
