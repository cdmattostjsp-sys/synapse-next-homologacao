# utils/relatorio_executivo_pdf.py
# ==========================================================
# SynapseNext – Fase Brasília (Passo 11E)
# Relatório Executivo em PDF institucional – TJSP / SAAB
# ==========================================================
import io
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfgen import canvas

def _on_page(canvas_obj: canvas.Canvas, doc):
    # Rodapé institucional
    canvas_obj.setFont("Helvetica", 8)
    w, h = A4
    rodape = f"TJSP | SAAB – vNext • {datetime.now().strftime('%d/%m/%Y')} • pág. {doc.page}"
    canvas_obj.drawRightString(w - 40, 25, rodape)

def _add_toc_entry(story, level, text):
    # helper para registrar headings no TOC
    # (o SimpleDocTemplate aceita afterFlowable)
    pass

def gerar_relatorio_executivo(dados_governanca, dados_alertas, dados_insights) -> str:
    """
    Gera um relatório executivo consolidado (PDF) e retorna o caminho absoluto.
    Espera estruturas já consolidadas nos dicionários de entrada.
    """
    out_dir = Path(__file__).resolve().parents[1] / "exports" / "relatorios"
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    pdf_path = out_dir / f"relatorio_executivo_{ts}.pdf"

    doc = SimpleDocTemplate(
        str(pdf_path), pagesize=A4,
        rightMargin=40, leftMargin=40, topMargin=60, bottomMargin=40
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Titulo", fontSize=16, leading=20, alignment=1, spaceAfter=12))
    styles.add(ParagraphStyle(name="Subtitulo", fontSize=11, leading=14, alignment=1, textColor=colors.grey))
    styles.add(ParagraphStyle(name="Heading1", parent=styles["Heading1"], spaceBefore=12, spaceAfter=6))
    styles.add(ParagraphStyle(name="Heading2", parent=styles["Heading2"], spaceBefore=10, spaceAfter=4))

    story = []

    # Capa
    story.append(Spacer(1, 100))
    story.append(Paragraph("<b>Relatório Executivo – SynapseNext</b>", styles["Titulo"]))
    story.append(Paragraph("Fase Brasília • SAAB 5.0 • Tribunal de Justiça de São Paulo", styles["Subtitulo"]))
    story.append(Spacer(1, 200))
    story.append(Paragraph(datetime.now().strftime("%d/%m/%Y"), styles["Subtitulo"]))
    story.append(PageBreak())

    # Sumário (TOC)
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle(fontSize=11, name='TOCLevel1', leftIndent=20, firstLineIndent=-10, spaceAfter=4),
        ParagraphStyle(fontSize=10, name='TOCLevel2', leftIndent=40, firstLineIndent=-10, spaceAfter=2),
    ]
    story.append(Paragraph("Sumário", styles["Heading1"]))
    story.append(toc)
    story.append(PageBreak())

    # 1. Introdução e Contexto
    story.append(Paragraph("1. Introdução e Contexto", styles["Heading1"]))
    story.append(Paragraph(
        "Este relatório consolida indicadores de governança, alertas proativos e insights históricos "
        "gerados nas fases 10 a 11D do projeto SynapseNext.", styles["BodyText"]
    ))
    story.append(Spacer(1, 12))

    # 2. Indicadores de Governança (exemplo de tabela)
    story.append(Paragraph("2. Indicadores de Governança", styles["Heading1"]))
    gov_resumo = dados_governanca.get("resumo", {})
    if gov_resumo:
        data = [["Indicador", "Valor"]]
        for k, v in gov_resumo.items():
            data.append([str(k), str(v)])
        tbl = Table(data, hAlign="LEFT")
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
            ("GRID", (0,0), (-1,-1), 0.25, colors.grey),
            ("BOTTOMPADDING", (0,0), (-1,0), 6),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 12))

    # 3. Alertas Proativos (gráfico + tabela)
    story.append(Paragraph("3. Alertas Proativos", styles["Heading1"]))
    tot = dados_alertas.get("totais", {"alto":0, "medio":0, "baixo":0})
    fig, ax = plt.subplots()
    ax.bar(["Altos", "Médios", "Baixos"], [tot.get("alto",0), tot.get("medio",0), tot.get("baixo",0)])
    ax.set_title("Distribuição de Alertas por Severidade")
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format="png", bbox_inches="tight")
    plt.close(fig)
    img_buf.seek(0)
    story.append(Image(img_buf, width=420, height=240))
    story.append(Spacer(1, 8))

    detalhes = dados_alertas.get("detalhes", [])
    if detalhes:
        header = ["Severidade", "Artefato", "Descrição"]
        data = [header] + [[d.get("sev","-"), d.get("artefato","-"), d.get("descricao","-")] for d in detalhes]
        tbl = Table(data, colWidths=[70, 120, 260])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
            ("GRID", (0,0), (-1,-1), 0.25, colors.grey),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 12))

    # 4. Insights Históricos (exemplo de série)
    story.append(Paragraph("4. Insights Históricos", styles["Heading1"]))
    serie = dados_insights.get("coerencia_global_mm", [])  # lista de floats
    if serie:
        fig2, ax2 = plt.subplots()
        ax2.plot(range(1, len(serie)+1), serie)
        ax2.set_title("Coerência Global – Média Móvel")
        ax2.set_xlabel("Períodos")
        ax2.set_ylabel("Índice")
        img2 = io.BytesIO()
        plt.savefig(img2, format="png", bbox_inches="tight")
        plt.close(fig2)
        img2.seek(0)
        story.append(Image(img2, width=420, height=240))
        story.append(Spacer(1, 12))

    # 5. Conclusão e Recomendações
    story.append(Paragraph("5. Conclusão e Recomendações", styles["Heading1"]))
    story.append(Paragraph(
        "Recomenda-se manter o ciclo de auditorias e comparações semânticas, priorizando a mitigação dos alertas de "
        "severidade alta e a melhoria contínua dos indicadores de coerência.", styles["BodyText"]
    ))
    story.append(Spacer(1, 12))
    story.append(Paragraph("TJSP | SAAB – Relatório Executivo vNext", styles["Subtitulo"]))

    # Hook para popular TOC conforme headings
    def after_flowable(flowable):
        if isinstance(flowable, Paragraph):
            text = flowable.getPlainText()
            style_name = flowable.style.name
            if style_name == "Heading1":
                level = 0
            elif style_name == "Heading2":
                level = 1
            else:
                return
            # notifica o TOC
            toc.addEntry(level, text, doc.page)

    doc.build(story, onFirstPage=_on_page, onLaterPages=_on_page, afterFlowable=after_flowable)
    return str(pdf_path)
