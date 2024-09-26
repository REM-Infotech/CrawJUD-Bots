import fitz  # PyMuPDF
from PIL import Image
import os
import pathlib
# Caminhos dos arquivos

def crop_itau(pdf: str) -> str:
    
    output_img = pdf.replace(".pdf", ".png")
    # Defina as coordenadas para cortar o PDF
    x0, y0 = 0, 0
    x1, y1 = 595, 425  # As coordenadas (595, 350) são baseadas em 8.5 x 11 polegadas a 72 dpi

    # Abre o documento PDF
    doc = fitz.open(pdf)
    page = doc.load_page(0)  # Carrega a primeira página

    # Define a área de corte (em pontos)
    rect = fitz.Rect(x0, y0, x1, y1)

    # Aplica o corte na página
    page.set_cropbox(rect)

    # Renderiza a página como uma imagem
    pix = page.get_pixmap()

    # Converte a imagem para o formato PIL
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # Salva a imagem
    image.save(output_img)

    return output_img

import fitz  # PyMuPDF
from PIL import Image
import os
import pathlib
# Caminhos dos arquivos

def crop_itau(pdf: str) -> str:
    
    output_img = pdf.replace(".pdf", ".png")
    # Defina as coordenadas para cortar o PDF
    x0, y0 = 0, 0
    x1, y1 = 595, 425  # As coordenadas (595, 350) são baseadas em 8.5 x 11 polegadas a 72 dpi

    # Abre o documento PDF
    doc = fitz.open(pdf)
    page = doc.load_page(0)  # Carrega a primeira página

    # Define a área de corte (em pontos)
    rect = fitz.Rect(x0, y0, x1, y1)

    # Aplica o corte na página
    page.set_cropbox(rect)

    # Renderiza a página como uma imagem
    pix = page.get_pixmap()

    # Converte a imagem para o formato PIL
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # Salva a imagem
    image.save(output_img)

    return output_img