""" Imports do Projeto """
from bot.head.Tools.PrintLogs import printtext as prt

from datetime import datetime
from typing import Type
from time import sleep
import time
import re
import os
from contextlib import suppress
import shutil
from PyPDF2 import *

# Selenium Imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement
from bot.head.common.exceptions import ErroDeExecucao
from selenium.webdriver.support import expected_conditions as EC
from bot.head.common.selenium_excepts import webdriver_exepts
from bot.head.common.selenium_excepts import exeption_message
from selenium.common.exceptions import NoSuchElementException


class movimentacao:

    def __init__(self, Initbot) -> None:
        
        self.__dict__ = Initbot.__dict__.copy()
        self.start_time = time.perf_counter()
    
    def execution(self):
        
        self.row = 2
        while not self.thread._is_stopped:
            if self.row == self.ws.max_row+1:
                self.prt = prt(self.pid, self.row)
                break
            
            self.appends = []
            self.resultados = []
            
            self.bot_data = {}
            for index in range(1, self.ws.max_column + 1):
                self.index = index
                self.bot_data.update(self.set_data())
                if index == self.ws.max_column:
                    break
            
            try:
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
                
                self.type_log = "error"
                self.message = f'{self.message}. | Operação: {old_message}'
                self.prt(self)()
                self.append_error([self.bot_data.get('NUMERO_PROCESSO'), self.message])
            
            self.row += 1
            
        self.finalize_execution()
    
    def queue(self) -> None:
        
        self.table_moves = None
        
        self.search(self.bot_data, self.prt)
        
        self.message = 'Buscando movimentações'
        self.prt.print_log("log", self.message)
        
        if self.bot_data.get("DATA_LIMITE"):
            self.extract_with_rangedata()
            
        elif self.bot_data.get("NOME_MOV"):
            self.get_textodoc()
            
        else:
            self.get_moves()
            
        self.append_moves()

    def set_page_size(self) -> None:

        select = Select(self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select[name="pagerConfigPageSize"]'))))
        select.select_by_value("1000")
    
    def extract_with_rangedata(self) -> None:
        
        data_inicio:WebElement = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[id="dataInicialMovimentacaoFiltro"]')))
        data_inicio.send_keys(self.bot_data.get("DATA_PUBLICACAO"))
        
        data_fim = self.driver.find_element(By.CSS_SELECTOR, 'input[id="dataFinalMovimentacaoFiltro"]')
        data_fim.send_keys(self.bot_data.get("DATA_LIMITE"))
        
        filtrar_button = self.driver.find_element(By.CSS_SELECTOR, 'input[id="editButton"]')
        filtrar_button.click()
        
        self.set_page_size()
        self.set_tablemoves()
  
        for move in self.table_moves:
            move: WebElement = move
            itensmove = move.find_elements(By.TAG_NAME, 'td')   
            
            if len(itensmove) < 5:
                continue
            data_mov = itensmove[2].text.split(" ")[0]
            text_mov = itensmove[3].text
            intimado = self.bot_data.get("INTIMADO", None) 
            if intimado is not None and not str(intimado).lower() in text_mov.lower():
                continue
            nome_mov = itensmove[3].find_element(By.TAG_NAME, "b").text
            movimentador = itensmove[4].text 
            seq = itensmove[1].text 
            if "SISTEMA PROJUDI" in movimentador:
                movimentador = movimentador.replace("  ", "")
                qualificacao_movimentador = movimentador
                
            elif "\n" in movimentador:
                info_movimentador =  movimentador.split("\n ")
                movimentador = info_movimentador[0].replace("  ", "")
                qualificacao_movimentador = info_movimentador[1]

            if str(self.bot_data.get("TRAZER_TEOR", "NÃO")).upper() == "SIM":
                def checkifdoc(texto: str) -> list:
                    
                    padrao = r'Referente ao evento (.+?) \((\d{2}/\d{2}/\d{4})\)'
                    
                    match = re.findall(padrao, texto)
                    
                    if len(match) == 0:
                        texto = "Referente ao evento (seq. 28) JUNTADA DE ATO ORDINATÓRIO (27/05/2024)"

                        # Regex para capturar o nome do evento e a data
                        pattern = r"\) ([A-Z\s]+) \((\d{2}/\d{2}/\d{4})\)"

                        # Aplicando a regex ao texto
                        match = re.findall(pattern, texto)
                    
                    return match

                checkdoc = checkifdoc(text_mov)
                if len(checkdoc) > 0:
                    self.resultados = checkdoc
                    self.get_textodoc()
                
            data = [self.bot_data.get("NUMERO_PROCESSO"), data_mov, nome_mov, text_mov, movimentador, qualificacao_movimentador]
            self.appends.append(data)
    
    def get_moves(self) -> None:

        encontrado = False
        
        self.set_page_size()
        self.set_tablemoves()
        
        palavras_chave = [str(self.bot_data.get("PALAVRA_CHAVE"))]
        if "," in self.bot_data.get("PALAVRA_CHAVE"):
            palavras_chave = str(self.bot_data.get("PALAVRA_CHAVE")).split(",")
            
        for palavra_chave in palavras_chave:
            
            for move in self.table_moves:
                move: WebElement = move
                itensmove = move.find_elements(By.TAG_NAME, 'td')   
                
                if len(itensmove) < 5:
                    continue
                data_mov = itensmove[2].text.split(" ")[0]
                if data_mov == self.bot_data.get("DATA_PUBLICACAO", data_mov):
                    text_mov = itensmove[3].text
                    if palavra_chave.lower() in text_mov.lower():
                        
                        encontrado = True
                        intimado = self.bot_data.get("INTIMADO", None) 
                        if intimado is not None and not intimado.lower() in text_mov.lower():
                            continue
                        nome_mov = itensmove[3].find_element(By.TAG_NAME, "b").text
                        movimentador = itensmove[4].text 
                        seq = itensmove[1].text 
                        if "SISTEMA PROJUDI" in movimentador:
                            movimentador = movimentador.replace("  ", "")
                            qualificacao_movimentador = movimentador
                            
                        elif "\n" in movimentador:
                            info_movimentador =  movimentador.split("\n ")
                            movimentador = info_movimentador[0].replace("  ", "")
                            qualificacao_movimentador = info_movimentador[1]

                        if str(self.bot_data.get("TRAZER_TEOR", "NÃO")).upper() == "SIM":
                            def checkifdoc(texto: str) -> list:
                                
                                padrao = r'Referente ao evento (.+?) \((\d{2}/\d{2}/\d{4})\)'
                                return re.findall(padrao, texto)

                            checkdoc = checkifdoc(text_mov)
                            if len(checkdoc) > 0:
                                self.resultados = checkdoc
                                self.get_textodoc()
                            
                        data = [self.bot_data.get("NUMERO_PROCESSO"), data_mov, nome_mov, text_mov, movimentador, qualificacao_movimentador]
                        self.appends.append(data)
        
        if encontrado is False:
            
            self.message = "Nenhuma movimentação encontrada"
            self.append_error([self.bot_data.get("NUMERO_PROCESSO", self.message)])
            
                   
    def get_textodoc(self) -> None:
        
        self.set_page_size()
        self.set_tablemoves()
        
        data = None
        if len(self.resultados) > 0:
            eventos = [str(self.resultados[0][0])]
            
            
            if ") " in str(self.resultados[0][0]):
                eventos = [str(self.resultados[0][0]).split(") ")[1]]
                
        if self.bot_data.get("NOME_MOV"):
            
            eventos = [self.bot_data.get("NOME_MOV")]
            if "," in self.bot_data.get("NOME_MOV"):
                eventos = str(self.bot_data.get("NOME_MOV")).replace(", ", ",").split(",")

        for evento in eventos:
            for move in self.table_moves:
                move: WebElement = move
                itensmove = move.find_elements(By.TAG_NAME, 'td')  
                
                if len(itensmove) != 5:
                    continue

                data_mov = itensmove[2].text.split(" ")[0]
                
                if len(self.resultados) == 0:
                    data = data_mov
                
                if data_mov == data:
                    text_mov = itensmove[3].find_element(By.TAG_NAME, 'b').text
                    
                    if not evento:
                        evento = text_mov
                    
                    splitedevento = evento.upper().split(" ") if " " in evento else [evento]
                    
                    if evento.upper() in text_mov.upper():
                        movimentador = itensmove[4].text 
                        seq = itensmove[1].text
                        nome_mov = text_mov
                        if "SISTEMA PROJUDI" in movimentador:
                            movimentador = movimentador.replace("  ", "")
                            qualificacao_movimentador = movimentador
                            
                        elif "\n" in movimentador:
                            info_movimentador =  movimentador.split("\n ")
                            movimentador = info_movimentador[0].replace("  ", "")
                            qualificacao_movimentador = info_movimentador[1]
                        
                        expand = None
                        with suppress(NoSuchElementException):
                            expand = move.find_element(By.CSS_SELECTOR, 'a[href="javascript://nop/"]')
                        
                        if expand is None:
                            text_mov = itensmove[3].text
                            data = [self.bot_data.get("NUMERO_PROCESSO"), data_mov, nome_mov, text_mov, movimentador, qualificacao_movimentador]
                            self.append_success(data, message=f'Movimentação SEQ.{seq} adicionado na planilha!')  
                            break   

                        expandattrib = expand.get_attribute('class')
                        id_tr = expandattrib.replace("linkArquivos", "row")
                        css_tr = f'tr[id="{id_tr}"]'

                        table_docs: WebElement = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_tr)))
                        style_expand = table_docs.get_attribute('style')
                        
                        if style_expand == 'display: none;':
                        
                            expand.click()
                            sleep(0.5)
                            table_docs: WebElement = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_tr)))
                        
                        rows = table_docs.find_elements(By.TAG_NAME, 'tr')
                        for docs in rows:
                            doc = docs.find_elements(By.TAG_NAME, 'td')[4]
                            link_doc = doc.find_element(By.TAG_NAME, 'a')
                            name_pdf = str(link_doc.text).replace(" ", "").replace("_", "")
                            url = link_doc.get_attribute("href")
                            nomearquivo = f"{self.bot_data.get('NUMERO_PROCESSO')} - SEQ.{seq} - {evento.upper()} - {self.pid}.pdf"
                            old_pdf = os.path.join(self.output_dir_path, name_pdf)
                            path_pdf = os.path.join(self.output_dir_path, nomearquivo)
                            
                            if not os.path.exists(path_pdf):   
                                
                                self.driver.get(url)
                                while  True:
                                    if os.path.exists(old_pdf):
                                        break
                                    sleep(0.01)   
                                    
                                    
                            shutil.move(old_pdf, path_pdf)
                            text_mov = self.openfile(path_pdf)
                            
                            if str(self.bot_data.get("TRAZER_DOC", "NÃO")).upper() == "NÃO" and not self.bot_data.get("NOME_MOV", None):
                                os.remove(path_pdf)
                                
                            data = [self.bot_data.get("NUMERO_PROCESSO"), data_mov, nome_mov, text_mov, movimentador, qualificacao_movimentador]
                            self.appends.append(data)
                                               
    def openfile(self, path_pdf: str) -> str:
        
        with open(path_pdf, 'rb') as pdf:
            read = PdfReader(pdf)
            #Read PDF
            pagescontent = ""
            for page in read.pages:
                try:
                    text = page.extract_text()
                    remove_n_space = text.replace("\n", " ")
                    pagescontent = pagescontent + remove_n_space
                except:
                    pass
            
        return pagescontent
    
    # def gpt_chat(self, text_mov: str) -> str:
        
    #     try:
            
    #         client = self.client()
            
    #         completion = client.chat.completions.create(
    #         model="gpt-3.5-turbo",
    #         messages=[
    #             {"role": "system", "content": "Você é expert em análise juridica, você sabe identificar dispotivos de sentença e decisões interlocutórias"},
    #             {"role": "user", "content": f":Poderia extrair o dispositivo desse texto aqui? {text_mov} Eu quero unicamente o texto, sem você falando qualquer coisa"},
    #             {"role": "user", "content": "Eu quero o texto ipsis litteris, sem resumos seus"}
    #         ]
    #         )
            
    #         text = completion.choices[0].message.content
    #         return text
    #     except Exception as e:
    #         print(e)
    #         return text_mov

    def set_tablemoves(self) -> None:
        
        self.table_moves = self.driver.find_element(By.CLASS_NAME, 'resultTable')
        self.table_moves = self.table_moves.find_elements(By.XPATH, './/tr[contains(@class, "odd") or contains(@class, "even")][not(@style="display:none;")]') 
