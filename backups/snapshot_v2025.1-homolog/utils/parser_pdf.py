# -*- coding: utf-8 -*-
"""
parser_pdf.py — versão estável
Extrator PDF universal usado pelo módulo INSUMOS.
Sempre retorna STRING.
"""

import fitz  # PyMuPDF

def extract_text_from_pdf(path: str) -> str:
    """
    Extrai texto de um PDF local.
    SEMPRE retorna string.
    Em caso de erro, retorna string vazia.
    """

    try:
        texto_final = []

        with fitz.open(path) as pdf:
            for page in pdf:
                texto_final.append(page.get_text())

        return "\n".join(texto_final).strip()

    except Exception as e:
        # Caso dê erro, retorna string vazia (NUNCA dict)
        return ""
