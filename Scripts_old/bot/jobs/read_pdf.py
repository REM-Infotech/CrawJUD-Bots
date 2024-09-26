import os
from PyPDF2 import *
import re
import openpyxl

def get_barcode(pdf1: str, pdf2: str, wscodbars: str, numproc: str):
    # Inicialize uma lista para armazenar os números encontrados
    bar_code = ''
    numeros_encontrados = []

    # Expressão regular para encontrar números nesse formato
    pattern = r'\b\d{5}\.\d{5}\s*\d{5}\.\d{6}\s*\d{5}\.\d{6}\s*\d\s*\d{14}\b'
    value_pattern = re.compile(r'(\d{1,3}(?:\.\d{3})*,\d{2})')

    with open(pdf1, "rb") as pdf1:
        read = PdfReader(pdf1)
        text = None
        values = None
        bar_code1 = ""
        bar_code2 = ""
        for page in read.pages:
            text1 = page.extract_text()
            
            try:
                # Use a expressão regular para encontrar números
                numeros = re.findall(pattern, text1)
                # Adicione os números encontrados à lista
            except:
                pass
            
            if len(numeros) == 0:
                for pattern2 in [r'\b\d{47}\b', r'\b\d{5}\s\d{5}\s*\d{5}\s\d{6}\s*\d{5}\s\d{6}\s*\d\s*\d{14}\b']:
                    # Use a expressão regular para encontrar números
                    numeros = re.findall(pattern2, text1)
            
                    numeros_encontrados.extend(numeros)
                    text = text1
            
        for numero in numeros_encontrados:
            numero = str(numero)
            bar_code1 = numero.replace("  ","").replace(" ","").replace(".", "")
            
    with open(pdf2, "rb") as pdf2:
    
        read = PdfReader(pdf2)

        for page in read.pages:
            text2 = page.extract_text()
            
            try:
                # Use a expressão regular para encontrar números
                numeros = re.findall(pattern, text2)
                
                # Adicione os números encontrados à lista
                numeros_encontrados.extend(numeros)
            except:
                pass
            
        for numero in numeros_encontrados:
            numero = str(numero)
            bar_code2 = numero.replace("  ","").replace(" ","").replace(".", "") 
        
    if bar_code1 == bar_code2:
        # Find all matches in the text
        values = value_pattern.findall(text)
        if len(values) > 0:
            values = values[0]
            wb = openpyxl.load_workbook(filename=wscodbars)
            sheet = wb.active
            data = [numproc, bar_code1, bar_code2]
            sheet.append(data)
            wb.save(wscodbars)
    
    return values