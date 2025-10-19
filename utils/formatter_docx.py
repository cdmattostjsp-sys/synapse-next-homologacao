# utils/formatter_docx.py
# ==========================================================
# SynapseNext – Fase Brasília
# Formatter institucional para exportação .docx com padrão TJSP
# ==========================================================

from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime
from pathlib import Path
import markdown

# ==========================================================
# Função principal
# ==========================================================
def markdown_to_docx(markdown_text: str, output_path: str, artefato_nome: str = "Documento") -> None:
    """
    Converte texto Markdown em documento .docx institucional com padrão TJSP.
    Inclui capa, cabeçalho, rodapé e formatação.
    """

    # Conversão básica markdown → texto bruto (mantém quebras de linha)
    html = markdown.markdown(markdown_text)
    lines = markdown_text.split("\n")

    doc = Document()

    # ==========================================================
    # Capa institucional
    # ==========================================================
    section = doc.sections[0]
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1.1)
    section.right_margin = Inches(1.1)

    logo_path = Path(__file__).resolve().parents[1] / "assets" / "tjsp_logo.png"
    if logo_path.exists():
        try:
            doc.add_picture(str(logo_path), width=Inches(1.1))
        except Exception:
            pass

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run("TRIBUNAL DE JUSTIÇA DO ESTADO DE SÃO PAULO\n")
    run_title.bold = True
    run_title.font.size = Pt(14)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = p_sub.add_run(f"{artefato_nome} – SynapseNext | Fase Brasília\n\n")
    run_sub.font.size = Pt(11)

    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_date = p_date.add_run(datetime.now().strftime("Gerado em %d/%m/%Y às %H:%M\n"))
    run_date.italic = True
    run_date.font.size = Pt(10)

    doc.add_page_break()

    # ==========================================================
    # Corpo do documento
    # ==========================================================
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Títulos
        if line.startswith("# "):
            p = doc.add_paragraph(line[2:].strip())
            p.style = "Heading 1"
        elif line.startswith("## "):
            p = doc.add_paragraph(line[3:].strip())
            p.style = "Heading 2"
        elif line.startswith("### "):
            p = doc.add_paragraph(line[4:].strip())
            p.style = "Heading 3"
        else:
            p = doc.add_paragraph(line)
            p.style = "Normal"
            for run in p.runs:
                run.font.name = "Calibri"
                run.font.size = Pt(11)

    # ==========================================================
    # Rodapé institucional
    # ==========================================================
    section = doc.sections[0]
    footer = section.footer.paragraphs[0]
    footer.text = "Gerado automaticamente pelo SynapseNext – SAAB 5.0 | Tribunal de Justiça do Estado de São Paulo"
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer.runs[0].font.size = Pt(9)
    footer.runs[0].italic = True

    # ==========================================================
    # Salvamento final
    # ==========================================================
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    doc.save(output_path)
