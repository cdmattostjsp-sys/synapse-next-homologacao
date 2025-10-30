"""
formatter_docx.py – SynapseNext vNext
Gerador e formatador de relatórios técnicos em formato DOCX
Homologado: SAAB/TJSP – 2025-10-29
"""

from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os
from datetime import datetime

EXPORTS_RELATORIOS = "exports/relatorios"
os.makedirs(EXPORTS_RELATORIOS, exist_ok=True)

def criar_documento(titulo_principal: str):
    """Cria e retorna um objeto Document com formatação inicial padrão SAAB/TJSP."""
    doc = Document()
    # Configura margens padrão
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Cabeçalho institucional
    titulo = doc.add_heading(titulo_principal, level=1)
    titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph(f"Data de emissão: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    doc.add_paragraph("Órgão: Secretaria de Administração e Abastecimento – SAAB/TJSP\n")

    return doc


def adicionar_secao(doc: Document, titulo: str, conteudo: str):
    """Adiciona uma nova seção ao documento com título e texto."""
    doc.add_heading(titulo, level=2)
    paragrafo = doc.add_paragraph(conteudo)
    paragrafo.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    paragrafo_format = paragrafo.paragraph_format
    paragrafo_format.space_after = Pt(8)
    return doc


def adicionar_lista(doc: Document, titulo: str, itens: list):
    """Adiciona uma lista com marcadores sob um título."""
    doc.add_heading(titulo, level=2)
    for item in itens:
        doc.add_paragraph(f"• {item}", style="List Bullet")
    return doc


def adicionar_assinatura(doc: Document, nome: str = "Synapse.Engineer", cargo: str = "Engenheiro Responsável"):
    """Adiciona a assinatura técnica institucional."""
    doc.add_paragraph("\n")
    assinatura = doc.add_paragraph()
    assinatura.add_run("_________________________________________\n").bold = True
    assinatura.add_run(f"{nome}\n{cargo}\nSAAB/TJSP").italic = True
    assinatura.alignment = WD_ALIGN_PARAGRAPH.CENTER
    return doc


def salvar_documento(doc: Document, nome_base: str):
    """Salva o documento com nome padronizado no diretório exports/relatorios."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    nome_arquivo = f"{nome_base}_{timestamp}.docx"
    caminho = os.path.join(EXPORTS_RELATORIOS, nome_arquivo)
    doc.save(caminho)
    print(f"✅ Relatório gerado com sucesso: {caminho}")
    return caminho


def gerar_relatorio_basico(titulo: str, secoes: dict, listas: dict = None):
    """
    Gera um relatório DOCX básico com título, seções e listas.
    Exemplo de uso:
        secoes = {"Objetivo": "...", "Diagnóstico": "..."}
        listas = {"Etapas": ["Passo 1", "Passo 2"]}
    """
    doc = criar_documento(titulo)
    for titulo_secao, conteudo in secoes.items():
        adicionar_secao(doc, titulo_secao, conteudo)

    if listas:
        for titulo_lista, itens in listas.items():
            adicionar_lista(doc, titulo_lista, itens)

    adicionar_assinatura(doc)
    return salvar_documento(doc, titulo.replace(" ", "_"))


if __name__ == "__main__":
    print("===================================================")
    print("📘 Teste de Geração – formatter_docx.py (SynapseNext vNext)")
    print("===================================================\n")

    secoes_exemplo = {
        "Objetivo": "Este é um teste de geração de relatório DOCX no padrão institucional SAAB/TJSP.",
        "Diagnóstico": "O módulo formatter_docx.py está operacional e pronto para integração com o restante do sistema."
    }

    listas_exemplo = {
        "Próximos Passos": [
            "Restaurar módulos restantes da pasta utils/",
            "Gerar relatório técnico consolidado de homologação",
            "Executar integração com painéis Streamlit"
        ]
    }

    gerar_relatorio_basico("Relatório de Teste – SynapseNext vNext", secoes_exemplo, listas_exemplo)
