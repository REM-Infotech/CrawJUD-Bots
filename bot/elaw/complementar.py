""" Crawler ELAW Cadastro"""

import os
import time
from time import sleep
from typing import Type
from contextlib import suppress


""" Imports do Projeto """
from bot.head import CrawJUD

from bot.head.Tools.PrintLogs import printtext as prt
from bot.head.common.exceptions import ErroDeExecucao
from bot.head.common.selenium_excepts import webdriver_exepts
from bot.head.common.selenium_excepts import exeption_message


# Selenium Imports
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import  NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC

type_doc = {
    11: "cpf",
    14: "cnpj"
}

lista1 = ["NUMERO_PROCESSO", "UNIDADE_CONSUMIDORA", "DIVISAO", 
          "DATA_CITACAO", "PROVIMENTO", "FASE", "FATO_GERADOR",
          "DESC_OBJETO", "OBJETO"]

class complement(CrawJUD):

    def __init__(self, Initbot: Type[CrawJUD]) -> None:
        
        self.__dict__ = Initbot.__dict__.copy()
        self.start_time = time.perf_counter()
        
    def execution(self):
        
        while not self.thread._is_stopped:
            if self.row == self.ws.max_row+1:
                self.prt = prt(self.pid, self.row)
                break
            
            self.bot_data = {}
            for index in range(1, self.ws.max_column + 1):
                self.index = index
                self.bot_data.update(self.set_data())
                if index == self.ws.max_column:
                    break
            
            try:
                
                if not len(self.bot_data) == 0:
                    self.prt = prt(self.pid, self.row-1, url_socket=self.argbot['url_socket'])
                    self.queue()
                
            except Exception as e:
                
                old_message = self.message
                self.message = getattr(e, 'msg', getattr(e, 'message', ""))
                if self.message == "":
                    for exept in webdriver_exepts():
                        if isinstance(e, exept):
                            self.message = exeption_message().get(exept)
                            break
                        
                if not self.message:
                    self.message = str(e)
                    
                error_message = f'{self.message}. | Operação: {old_message}'
                self.prt.print_log("error", error_message)
                self.append_error([self.bot_data.get('NUMERO_PROCESSO'), self.message])
            
            self.row += 1
            
        self.finalize_execution()
        
    def queue(self) -> None:

        search = self.search(self.bot_data, self.prt)
        
        if search is True:
                
            self.prt.print_log("log", "Inicializando complemento de cadastro")
            
            edit_proc_button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[id="dtProcessoResults:0:btnEditar"]')))
            edit_proc_button.click()
            
            start_time = time.perf_counter()

            complement_list = list(self.bot_data)
            
            ordenada_lista1 = [x for _, x in zip(complement_list, lista1)]
            for name in ordenada_lista1:
                
                name = str(name)
                func = None
                with suppress(AttributeError):
                    func = getattr(self, name.lower())
                
                if func is None:
                    continue
                    
                func()
            
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            calc = execution_time/60
            splitcalc = str(calc).split(".")
            minutes = int(splitcalc[0])
            seconds = int(float(f"0.{splitcalc[1]}") * 60)

            self.prt.print_log("log", f"Formulário preenchido em {minutes} minutos e {seconds} segundos")
            self.salvar_tudo()
            
            if self.confirm_save() is True:
                name_comprovante = self.print_comprovante()
                self.message = 'Processo salvo com sucesso!'
        
            self.append_success([self.bot_data.get("NUMERO_PROCESSO"), self.message, name_comprovante], self.message)
            
        else:
            self.message = "Processo não encontrado!"
            self.prt.print_log("error", self.message)
            self.append_error([self.bot_data.get("NUMERO_PROCESSO"), self.message])

    def unidade_consumidora(self) -> None:

        self.message = "Informando unidade consumidora"
        self.prt.print_log("log", self.message)

        css_input_uc = 'textarea[id="j_id_3k_1:j_id_3k_4_2_2_6_9_44_2:j_id_3k_4_2_2_6_9_44_3_1_2_2_1_1:j_id_3k_4_2_2_6_9_44_3_1_2_2_1_13"]'

        input_uc: WebElement = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, css_input_uc)))
        input_uc.click()
        
        self.interact.clear(input_uc)
        
        self.interact.send_key(input_uc, self.bot_data.get("UNIDADE_CONSUMIDORA"))

        self.message = "Unidade consumidora informada!"
        self.prt.print_log("log", self.message)

    def divisao(self) -> None:

        css_set_divisao = 'div[id="j_id_3k_1:j_id_3k_4_2_2_a_9_44_2:j_id_3k_4_2_2_a_9_44_3_1_2_2_1_1:fieldid_9241typeSelectField1CombosCombo"]'
        elemento = 'input[id="j_id_3k_1:j_id_3k_4_2_2_a_9_44_2:j_id_3k_4_2_2_a_9_44_3_1_2_2_1_1:fieldid_9241typeSelectField1CombosCombo_filter"]'
        self.message = "Informando divisão"
        self.prt.print_log("log", self.message)
        
        div_divisao: WebElement = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_set_divisao)))
        div_divisao.click()

        sleep(0.5)
        text = str(self.bot_data.get("DIVISAO"))
        
        elemento: WebElement = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, elemento)))
        elemento.click()
        
        self.interact.clear(elemento)
        self.interact.send_key(elemento, text)
        self.interact.send_key(elemento, Keys.ENTER)
        
        self.interact.sleep_load('div[id="j_id_3x"]')

        self.message = "Divisão informada!"
        self.prt.print_log("log", self.message)

    def data_citacao(self) -> None:

        self.message = "Informando data de citação"
        self.prt.print_log('log', self.message)

        css_data_citacao = 'input[id="j_id_3k_1:dataRecebimento_input"]'

        data_citacao: WebElement = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_data_citacao)))
        self.interact.clear(data_citacao)
        self.interact.sleep_load('div[id="j_id_3x"]')
        self.interact.send_key(data_citacao, self.bot_data.get("DATA_CITACAO"))
        sleep(2)
        self.driver.execute_script(f"document.querySelector('{css_data_citacao}').blur()")
        self.interact.sleep_load('div[id="j_id_3x"]')
        
        self.message = "Data de citação informada!"
        self.prt.print_log('log', self.message)
    
    def fase(self) -> None:

        """Declaração dos CSS em variáveis"""
        processoFaseCombo = 'div[id="j_id_3k_1:processoFaseCombo"]'
        elemento = 'div[id="j_id_3k_1:processoFaseCombo_panel"]'
        
        self.message = "Informando fase do processo"
        self.prt.print_log('log', self.message)
        
        div_fase: WebElement = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, processoFaseCombo)))
        self.interact.double_click(div_fase)
        sleep(1)
        
        text = self.bot_data.get("FASE", "INICIAL")
        self.interact.select_item(elemento, text)
        self.interact.sleep_load('div[id="j_id_3x"]')

        self.message = "Fase informada!"
        self.prt.print_log('log', self.message) 

    def provimento(self) -> None:

        """Declaração dos CSS em variáveis"""
        provimentoCombo = 'div[id="j_id_3k_1:j_id_3k_4_2_2_g_9_44_2:j_id_3k_4_2_2_g_9_44_3_1_2_2_1_1:fieldid_8401typeSelectField1CombosCombo"]'
        elemento = 'div[id="j_id_3k_1:j_id_3k_4_2_2_g_9_44_2:j_id_3k_4_2_2_g_9_44_3_1_2_2_1_1:fieldid_8401typeSelectField1CombosCombo_panel"]'
        
        self.message = "Informando provimento antecipatório"
        self.prt.print_log('log', self.message)
        
        tipo_entrada_Css = 'div[id="j_id_3k_1:j_id_3k_4_2_2_e_9_44_2:j_id_3k_4_2_2_e_9_44_3_1_2_2_1_1:fieldid_9242typeSelectField1CombosCombo"]'
        tipo_entrada = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, tipo_entrada_Css)))
        self.interact.scroll_to(tipo_entrada)
        
        div_provimento: WebElement = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, provimentoCombo)))
        div_provimento.click()
        sleep(1)
        
        text = self.bot_data.get("PROVIMENTO")
        self.interact.select_item(elemento, text)
        self.interact.sleep_load('div[id="j_id_3x"]')
        
        self.message = "Provimento antecipatório informado!"
        self.prt.print_log("log", self.message)    

    def fato_gerador(self) -> None:

        """Declaração dos CSS em variáveis"""
        fatogeradorCombo = 'div[id="j_id_3k_1:j_id_3k_4_2_2_m_9_44_2:j_id_3k_4_2_2_m_9_44_3_1_2_2_1_1:fieldid_9239typeSelectField1CombosCombo"]'
        elemento = 'div[id="j_id_3k_1:j_id_3k_4_2_2_m_9_44_2:j_id_3k_4_2_2_m_9_44_3_1_2_2_1_1:fieldid_9239typeSelectField1CombosCombo_panel"]'
        
        self.message = "Informando fato gerador"
        self.prt.print_log("log", self.message)

        
        div_fatogerador: WebElement = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, fatogeradorCombo)))
        div_fatogerador.click()
        sleep(1)
        
        text = self.bot_data.get("FATO_GERADOR")
        self.interact.select_item(elemento, text)
        self.interact.sleep_load('div[id="j_id_3x"]')

        self.message = "Fato gerador informado!"
        self.prt.print_log("log", self.message)    
    
    def desc_objeto(self) -> None:
        
        input_descobjeto_css = 'textarea[id="j_id_3k_1:j_id_3k_4_2_2_l_9_44_2:j_id_3k_4_2_2_l_9_44_3_1_2_2_1_1:j_id_3k_4_2_2_l_9_44_3_1_2_2_1_13"]'
        
        input_descobjeto = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, input_descobjeto_css)))
        self.interact.click(input_descobjeto)
        
        text = self.bot_data.get("OBJETO")
        self.interact.clear(input_descobjeto)
        self.interact.send_key(input_descobjeto, text)
        self.driver.execute_script(f"document.querySelector('{input_descobjeto_css}').blur()")
        self.interact.sleep_load('div[id="j_id_3x"]')
        
    def objeto(self) -> None:

        """Declaração dos CSS em variáveis"""
        objetoCombo = 'div[id="j_id_3k_1:j_id_3k_4_2_2_n_9_44_2:j_id_3k_4_2_2_n_9_44_3_1_2_2_1_1:j_id_3k_4_2_2_n_9_44_3_1_2_2_1_a"]'
        elemento = 'input[id="j_id_3k_1:j_id_3k_4_2_2_n_9_44_2:j_id_3k_4_2_2_n_9_44_3_1_2_2_1_1:fieldid_8405typeSelectField1CombosCombo_filter"]'
        
        self.message = "Informando objeto do processo"
        self.prt.print_log("log", self.message)
        
        div_objeto: WebElement = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, objetoCombo)))
        div_objeto.click()
        
        elemento = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, elemento)))
        
        text = self.bot_data.get("OBJETO")
        self.interact.click(elemento)
        self.interact.send_key(elemento, text)
        self.interact.send_key(elemento, Keys.ENTER)
        self.interact.sleep_load('div[id="j_id_3x"]')
        
        self.message = "Objeto do processo informado!"
        self.prt.print_log("log", self.message)

    def salvar_tudo(self) -> None:

        self.interact.sleep_load('div[id="j_id_3x"]')
        css_salvar_proc = 'button[id="btnSalvarOpen"]'
        salvartudo: WebElement = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, css_salvar_proc)))
        self.prt.print_log("log", "Salvando processo novo")
        salvartudo.click()

    def print_comprovante(self) -> str:

        name_comprovante = f'Comprovante Cadastro - {self.bot_data.get("NUMERO_PROCESSO")} - PID {self.pid}.png'
        savecomprovante = os.path.join(os.getcwd(), 'Temp', self.pid, name_comprovante)
        self.driver.get_screenshot_as_file(savecomprovante)
        return name_comprovante

    def confirm_save(self) -> bool:
        
        wait_confirm_save = None

        with suppress(TimeoutException):
            wait_confirm_save:WebElement = WebDriverWait(self.driver, 20).until(
                EC.url_to_be(("https://amazonas.elaw.com.br/processoView.elaw")))

        if wait_confirm_save:
            return True

        else:
            div_messageerro_css = 'div[id="messages"]'
            try:
                message: WebElement = self.wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, div_messageerro_css))).find_element(By.TAG_NAME, "ul").text
                
                raise ErroDeExecucao(self.message)

            except Exception as e:
                self.message = "Processo Não cadastrado"
                raise ErroDeExecucao(self.message)
            
