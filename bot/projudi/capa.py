import re
import time
from typing import Type
from datetime import datetime


""" Imports do Projeto """

from bot.head.Tools.PrintLogs import printtext as prt
from bot.head.common.selenium_excepts import webdriver_exepts
from bot.head.common.selenium_excepts import exeption_message

# Selenium Imports
from selenium.webdriver.common.by import By
from bot.head import CrawJUD


class capa(CrawJUD):

    def __init__(self, Initbot: Type[CrawJUD]) -> None:
        
        self.__dict__ = Initbot.__dict__.copy()
        self.start_time = time.perf_counter()
    
    def execution(self):
        
        self.row = 2
        while not self.thread._is_stopped:
            
            if self.driver.title.lower() == "a sessao expirou":
                self.auth.set_portal()
            
            if self.row == self.ws.max_row+1:
                self.prt = prt(self.pid, self.ws.max_row, url_socket=self.argbot['url_socket'])
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
                
                old_message = str(self.message)
                self.message = str(getattr(e, 'msg', getattr(e, 'message', "")))
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
        
    def queue(self):
        
        self.search(self.bot_data, self.prt)
        self.driver.refresh()
        self.append_success(self.get_process_informations())

    def get_process_informations(self) -> list:

        self.prt.print_log("log", f"Obtendo informações do processo {self.bot_data.get('NUMERO_PROCESSO')}...") 

        navegar = self.driver.find_element(By.CSS_SELECTOR, '#tabItemprefix2')
        navegar.click()

        try:
            form = self.driver.find_element(By.ID, "includeContent")
        except:
            time.sleep(3)
            self.driver.refresh()
            time.sleep(1)
            form = self.driver.find_element(By.ID, "includeContent")

        tablePoloAtivo = form.find_elements(By.CLASS_NAME, "resultTable")[0]
        nomePoloAtivo = tablePoloAtivo.find_element(By.XPATH, ".//tbody").find_elements(By.XPATH, ".//tr")[0].find_elements(By.XPATH, ".//td")[1].text.replace('(citação online)', '')
        
        if " representado" in nomePoloAtivo:
            nomePoloAtivo = str(nomePoloAtivo.split(" representado")[0])
        
        cpfPoloAtivo = tablePoloAtivo.find_element(By.XPATH, ".//tbody").find_elements(By.XPATH, ".//tr")[0].find_elements(By.XPATH, ".//td")[3].text
        advPoloAtivo = tablePoloAtivo.find_element(By.XPATH, ".//tbody").find_elements(By.XPATH, ".//tr")[0].find_elements(By.XPATH, ".//td")[5].text

        tablePoloPassivo = form.find_elements(By.CLASS_NAME, "resultTable")[1]
        nomePoloPassivo = tablePoloPassivo.find_element(By.XPATH, ".//tbody").find_elements(By.XPATH, ".//tr")[0].find_elements(By.XPATH, ".//td")[1].text.replace('(citação online)', '')
        cpfPoloPassivo = tablePoloPassivo.find_element(By.XPATH, ".//tbody").find_elements(By.XPATH, ".//tr")[0].find_elements(By.XPATH, ".//td")[3].text

        navegar2 = self.driver.find_element(By.CSS_SELECTOR, '#tabItemprefix0')
        navegar2.click()

        try:
            form = self.driver.find_element(By.ID, "includeContent")
        except:
            time.sleep(3)
            self.driver.refresh()
            time.sleep(1)
            form = self.driver.find_element(By.ID, "includeContent")

        form = form.find_element(By.CLASS_NAME, "form")

        area_direito = str(form.find_elements(By.XPATH, ".//tr")[0].find_elements(By.XPATH, ".//td")[4].text)
        
        if area_direito.lower() == "juizado especial cível":
            
            area_direito = area_direito.lower().replace("juizado especial cível", "juizado especial").capitalize()
        
        foro = str(form.find_elements(By.XPATH, ".//tr")[1].find_elements(By.XPATH, ".//td")[4].text)
        
        comarca = foro
        
        if "je cível" in foro.lower():
            
            foro = foro.lower().replace("je cível", "cível").capitalize()
            
        if " da comarca de " in foro:
            comarca = foro.split(" da comarca de ")[1]
        
        if "cível" in comarca.lower():
            
            comarca = comarca.split(" - ")[0].capitalize()
        
        data_distribuicao = form.find_elements(By.XPATH, ".//tr")[2].find_elements(By.XPATH, ".//td")[1].text
        
        if " às " in data_distribuicao:
            data_distribuicao = data_distribuicao.split(" às ")[0]
            data_distribuicao = datetime.strptime(data_distribuicao, "%d/%m/%Y")
        
        
        infoproc = self.driver.find_element(By.CSS_SELECTOR,'table[id="informacoesProcessuais"]')
        tablestatusproc = infoproc.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME,'tr')[0]
        
        try:
            statusproc = tablestatusproc.find_elements(By.TAG_NAME, 'td')[1].text
        except:
            statusproc = 'Não Consta'
        try:
            juizproc = form.find_elements(By.XPATH, ".//tr")[2].find_elements(By.XPATH, ".//td")[4].text
        except:
            juizproc = 'Não Consta'
        
        try:
            form = self.driver.find_element(By.ID, "includeContent")
        except:
            time.sleep(3)
            self.driver.refresh()
            time.sleep(1)
            form = self.driver.find_element(By.ID, "includeContent")
        
        form = form.find_element(By.CLASS_NAME, "form").find_elements(By.TAG_NAME, "tr")
        
        for it in form:
            
            get_label = it.find_elements(By.TAG_NAME, "td")[0].text
            
            if get_label == "Valor da Causa:":
                
                valorDaCausa = str(it.find_elements(By.TAG_NAME, "td")[1].text)
                break
                
        assunto = self.driver.find_element(By.CSS_SELECTOR, 'a[class="definitionAssuntoPrincipal"]').text.split(" - ")[1]
        
        if "¤" in valorDaCausa:
            valorDaCausa = valorDaCausa.replace("¤", "")
        
        pattern = r'(?<!\S)(?:US\$[\s]?|R\$[\s]?|[\$]?)\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?(?!\S)'
        matches = re.findall(pattern, valorDaCausa)
        if len(matches) > 0:
            def convert_to_float(value):
                # Remover símbolos de moeda e espaços
                value = re.sub(r'[^\d.,]', '', value)
                
                # Identificar se o formato é BRL (com vírgula para decimais) ou USD (com ponto para decimais)
                if ',' in value and '.' in value:
                    # Assumir formato USD se houver tanto ',' quanto '.'
                    parts = value.split('.')
                    if len(parts[-1]) == 2:
                        value = value.replace(',', '')
                    else:
                        value = value.replace('.', '').replace(',', '.')
                elif ',' in value:
                    # Assumir formato BRL
                    value = value.replace('.', '').replace(',', '.')
                elif '.' in value:
                    # Assumir formato USD
                    value = value.replace(',', '')

                return float(value)
            
            valorDaCausa = convert_to_float(matches[0])
        
        if "vara única" in foro.lower():
            
            vara = foro.split(" da ")[0]
            
        else:
            
            vara = foro.split(" ")[0]
        
        if " - " in advPoloAtivo:
            
            get_oab = advPoloAtivo.split(" - ")[0]
            advPoloAtivo = advPoloAtivo.split(" - ")[1]
            
        elif advPoloAtivo == "Parte sem advogado":
            get_oab = ''

        processo_data = [self.bot_data.get('NUMERO_PROCESSO'), area_direito, "Geral", "Amazonas", comarca, foro, vara, data_distribuicao, nomePoloAtivo, "Autor",
                         cpfPoloAtivo, nomePoloPassivo, "réu", cpfPoloPassivo, statusproc, "Liliane Da Silva Roque", advPoloAtivo, "Fonseca Melo e Viana Advogados Associados", 
                         valorDaCausa]
        
        """
        
        return ["AREA_DIREITO", "SUBAREA_DIREITO", "ESTADO", "COMARCA", "FORO",
            "VARA", "DATA_DISTRIBUICAO", "PARTE_CONTRARIA", "TIPO_PARTE_CONTRARIA", "DOC_PARTE_CONTRARIA",
            "EMPRESA", "TIPO_EMPRESA", "DOC_EMPRESA", "ACAO", "ADVOGADO_INTERNO",
            "ADV_PARTE_CONTRARIA", "ESCRITORIO_EXTERNO", "VALOR_CAUSA"]
        
        """
        return processo_data


