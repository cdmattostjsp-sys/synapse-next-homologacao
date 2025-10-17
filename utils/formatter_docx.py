import os
from datetime import datetime
from io import BytesIO
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

# ===========================================
# 📁 DIRETÓRIO PADRÃO PARA SALVAR DOCUMENTOS
# ===========================================

OUTPUT_DIR = os.path.join(os.getcwd(), "outputs")
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR, exist_ok=True)


# ===========================================
# 🔧 FUNÇÃO PRINCIPAL – GERAR DOCUMENTO
# ===========================================

def markdown_to_docx(markdown_text: str, title: str = "Documento Synapse", summary: str = ""):
    """
    Converte o conteúdo validado (ou extraído via parser PDF) em um arquivo DOCX formatado.
    Compatível com DFD, ETP, TR e Contrato.
    Retorna o arquivo como buffer (para download no Streamlit) e o caminho salvo localmente.
    """
    document = Document()

    # === CABEÇALHO INSTITUCIONAL ===
    title_paragraph = document.add_paragraph(title)
    title_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_paragraph.runs[0].bold = True
    title_paragraph.runs[0].font.size = Pt(14)

    document.add_paragraph(f"Data de geração: {datetime.now().strftime('%d/%m/%Y')}")
    document.add_paragraph("Tribunal de Justiça do Estado de São Paulo – Secretaria de Administração e Abastecimento (SAAB)")
    document.add_paragraph("Projeto Synapse.IA – Ecossistema SAAB 5.0")
    document.add_paragraph("")

    # === CONTEÚDO PRINCIPAL ===
    lines = markdown_text.split("\n")
    for line in lines:
        if not line.strip():
            continue

        if line.startswith("# "):
            p = document.add_paragraph(line.replace("# ", ""), style="Heading1")
        elif line.startswith("## "):
            p = document.add_paragraph(line.replace("## ", ""), style="Heading2")
        elif line.startswith("### "):
            p = document.add_paragraph(line.replace("### ", ""), style="Heading3")
        elif line.startswith("💡"):
            p = document.add_paragraph(line, style="ListBullet")
        else:
            p = document.add_paragraph(line)
            p.paragraph_format.space_after = Pt(6)

    # === RESUMO OPCIONAL ===
    if summary:
        document.add_page_break()
        document.add_heading("Resumo e Recomendações", level=2)
        document.add_paragraph(summary)

    # === RODAPÉ PADRÃO ===
    document.add_paragraph("")
    document.add_paragraph("Gerado automaticamente pelo SynapseNext • SAAB/TJSP")
    document.add_paragraph("© Tribunal de Justiça do Estado de São Paulo – Todos os direitos reservados.")

    # === SALVAR E RETORNAR ===
    file_name = f"{title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
    file_path = os.path.join(OUTPUT_DIR, file_name)

    buffer = BytesIO()
    document.save(buffer)
    buffer.seek(0)
    document.save(file_path)

    return buffer, file_path
