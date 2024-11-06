""" Crawler ELAW Andamentos"""

import time
from time import sleep

from bot.CrawJUD import CrawJUD
from bot.common.exceptions import ErroDeExecucao
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC


class andamentos(CrawJUD):

    def __init__(self, **kwrgs) -> None:
        super().__init__(**kwrgs)
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
        if search is True:
            btn_newmove = (
                'button[id="tabViewProcesso:j_id_i3_4_1_3_ae:novoAndamentoPrimeiraBtn"]'
            )
            new_move: WebElement = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, btn_newmove))
            )
            new_move.click()

            self.info_data()
            self.info_ocorrencia()
            self.info_observacao()

            if self.bot_data.get("ANEXOS", None):
                self.add_anexo()

            self.save_andamento()

        elif search is not True:
            self.message = "Processo não encontrado!"
            self.type_log = "error"
            self.prt()
            self.append_error([self.bot_data.get("NUMERO_PROCESSO"), self.message])

    def info_data(self) -> None:

        try:

            self.message = "Informando data"
            self.type_log = "log"
            self.prt()
            css_Data = 'input[id="j_id_2n:j_id_2r_2_9_input"]'
            campo_data: WebElement = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_Data))
            )
            campo_data.click()
            campo_data.send_keys(Keys.CONTROL, "a")
            sleep(0.5)
            campo_data.send_keys(Keys.BACKSPACE)
            self.interact.send_key(campo_data, self.bot_data.get("DATA"))
            campo_data.send_keys(Keys.TAB)

            self.interact.sleep_load('div[id="j_id_34"]')

        except Exception as e:
            raise ErroDeExecucao(e=e)

    def info_ocorrencia(self) -> None:

        try:
            self.message = "Informando ocorrência"
            self.type_log = "log"
            self.prt()
            inpt_ocorrencia = 'textarea[id="j_id_2n:txtOcorrenciaAndamento"]'

            ocorrencia = self.driver.find_element(By.CSS_SELECTOR, inpt_ocorrencia)
            text_andamento = (
                str(self.bot_data.get("OCORRENCIA")).replace("\t", "").replace("\n", "")
            )

            self.interact.send_key(ocorrencia, text_andamento)

        except Exception as e:
            raise ErroDeExecucao(e=e)

    def info_observacao(self) -> None:

        try:
            self.message = "Informando observação"
            self.type_log = "log"
            self.prt()

            inpt_obs = 'textarea[id="j_id_2n:txtObsAndamento"]'

            observacao = self.driver.find_element(By.CSS_SELECTOR, inpt_obs)
            text_andamento = (
                str(self.bot_data.get("OBSERVACAO")).replace("\t", "").replace("\n", "")
            )

            self.interact.send_key(observacao, text_andamento)

        except Exception as e:
            raise ErroDeExecucao(e=e)

    def add_anexo(self) -> None:

        pass

    def save_andamento(self) -> None:

        try:
            self.message = "Salvando andamento..."
            self.type_log = "log"
            self.prt()
            sleep(1)
            self.link = self.driver.current_url
            save_button = self.driver.find_element(By.ID, "btnSalvarAndamentoProcesso")
            save_button.click()

        except Exception as e:
            raise ErroDeExecucao("Não foi possivel salvar andamento", e=e)

        try:
            check_save: WebElement = WebDriverWait(self.driver, 10).until(
                EC.url_to_be("https://amazonas.elaw.com.br/processoView.elaw")
            )
            if check_save:
                sleep(3)

                self.append_success(
                    [self.numproc, "Andamento salvo com sucesso!", ""],
                    "Andamento salvo com sucesso!",
                )

        except Exception:
            raise ErroDeExecucao(
                "Aviso: não foi possivel validar salvamento de andamento"
            )
