# streamlit_app/pages/Validador de Editais.py
# ==========================================================
# Validar Editais – SAAB 5.0 (TJSP)
# Página com validação semântica + checklist e exportação PDF
# ==========================================================

import sys
import io
from datetime import datetime
from pathlib import Path

import streamlit as st
from PIL import Image

# ----------------------------------------------------------
# Compatibilidade de import (acessa /utils e /knowledge no repo)
# ----------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# Tenta usar os validadores "oficiais". Se não existirem, usa fallback.
VALIDADOR_BASICO_OK = True
try:
    # Checklist (estrutural)
    from validators.edital_validator import validar_edital  # seu validador legado/novo

    # Semântica (IA/heurística)
    from knowledge.validators.edital_semantic_validator import (
        validar_semantica_edital,
    )
except Exception:
    VALIDADOR_BASICO_OK = False


# ----------------------------------------------------------
# Utilitários locais
# ----------------------------------------------------------
def carregar_logo() -> Image.Image | None:
    """
    Carrega o logotipo institucional (se existir).
    Busca primeiro em ./assets; se não achar, busca na raiz do projeto.
    """
    candidatos = [
        ROOT_DIR / "assets" / "tjsp_logo.png",
        Path.cwd() / "assets" / "tjsp_logo.png",
    ]
    for c in candidatos:
        if c.exists():
            try:
                return Image.open(c)
            except Exception:
                pass
    return None


def aplicar_css_basico():
    """
    Ajustes visuais padronizados: tipografia, espaçamento e botão acessível.
    """
    st.markdown(
        """
        <style>
        /* Títulos menores e com melhor espaçamento */
        h1, .stMarkdown h1 { font-size: 1.9rem !important; }
        h2, .stMarkdown h2 { font-size: 1.4rem !important; margin-top: 0.6rem !important; }
        h3, .stMarkdown h3 { font-size: 1.2rem !important; }

        /* Espaços mais contidos */
        .block-container { padding-top: 1.4rem; }
        .stMarkdown p { line-height: 1.45; }

        /* Botões acessíveis */
        .stButton > button {
            background-color: #003366 !important;
            color: #ffffff !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            padding: 0.55rem 1.25rem !important;
            border: none !important;
        }
        .stButton > button:hover {
            background-color: #002a55 !important;
            color: #ffffff !important;
        }

        /* Badges simples */
        .badge-ok {
            background: #e6f7ec; color: #1f7a3f; padding: 2px 8px; border-radius: 10px;
            border: 1px solid #bde5c8; font-size: 0.85rem;
        }
        .badge-attn {
            background: #fff7e6; color: #925d0b; padding: 2px 8px; border-radius: 10px;
            border: 1px solid #ffe1ac; font-size: 0.85rem;
        }
        .badge-crit {
            background: #fdecea; color: #a61b1b; padding: 2px 8px; border-radius: 10px;
            border: 1px solid #f5b5b0; font-size: 0.85rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def validar_fallback(tipo: str, texto: str) -> dict:
    """
    Fallback de validação quando não há módulos oficiais.
    Aplica algumas regras simples e retorna estrutura padronizada.
    """
    achados = []
    texto_lower = texto.lower()

    # Regras simples de demonstração
    regras = [
        ("Objeto definido", "objeto", "incluir uma seção clara sobre o objeto da contratação"),
        ("Prazo de execução", "prazo", "informar prazos de execução e vigência"),
        ("Critérios de julgamento", "critérios", "descrever os critérios de julgamento e pontuação"),
        ("Sanções/penalidades", "sanção", "detalhar sanções e penalidades aplicáveis"),
    ]
    for titulo, palavra, dica in regras:
        if palavra not in texto_lower:
            achados.append(
                {
                    "severidade": "Médio",
                    "secao": titulo,
                    "mensagem": f"Elemento não encontrado: **{titulo}**.",
                    "recomendacao": f"Sugestão: {dica}.",
                }
            )

    # score simples: mais faltas → menor score
    score = max(0, 100 - len(achados) * 18)
    status = "Conforme" if score >= 80 else "Atenções" if score >= 60 else "Crítico"

    return {
        "tipo": tipo,
        "score": score,
        "status": status,
        "achados": achados,
        "observacoes": "Validação básica aplicada (módulos oficiais indisponíveis).",
    }


def executar_validacao(tipo: str, modo: str, texto: str) -> dict:
    """
    Executa a validação usando os módulos oficiais. Se não existirem, usa fallback.
    Retorna um dicionário com:
      - score (0-100)
      - status ("Conforme", "Atenções", "Crítico")
      - achados: lista de dicts {severidade, secao, mensagem, recomendacao}
      - observacoes (string)
    """
    if not texto.strip():
        return {
            "tipo": tipo,
            "score": 0,
            "status": "Crítico",
            "achados": [
                {
                    "severidade": "Crítico",
                    "secao": "Conteúdo",
                    "mensagem": "Nenhum conteúdo foi informado para validação.",
                    "recomendacao": "Cole o texto (ou parte representativa) do edital para que a análise seja executada.",
                }
            ],
            "observacoes": "Sem conteúdo.",
        }

    if VALIDOR := VALIDOR  # noqa
    :
        pass  # apenas para manter linters quietos :)

    if VALIDADOR_BASICO_OK:
        # Estrutural/checklist
        try:
            checklist = validar_edital(tipo_contratacao=tipo, conteudo=texto)
        except Exception:
            checklist = {"achados": []}

        # Semântica
        try:
            semantica = validar_semantica_edital(tipo_contratacao=tipo, conteudo=texto, modo=modo)
        except Exception:
            semantica = {"achados": [], "score": 0}

        # Unificação
        achados = []
        for it in (checklist.get("achados", []) + semantica.get("achados", [])):
            # Garantir chaves padronizadas
            achados.append(
                {
                    "severidade": it.get("severidade", "Médio"),
                    "secao": it.get("secao", "Geral"),
                    "mensagem": it.get("mensagem", ""),
                    "recomendacao": it.get("recomendacao", ""),
                }
            )

        # Score/Status
        score_sem = semantica.get("score", 0)
        penalidade = sum(10 if a["severidade"] == "Crítico" else 5 if a["severidade"] == "Médio" else 2 for a in achados)
        score = max(0, min(100, score_sem - penalidade // 2))
        status = "Conforme" if score >= 80 else "Atenções" if score >= 60 else "Crítico"

        return {
            "tipo": tipo,
            "score": score,
            "status": status,
            "achados": achados,
            "observacoes": "Validação executada com módulos oficiais.",
        }

    # Fallback
    return validar_fallback(tipo, texto)


def badge_status(status: str) -> str:
    if status == "Conforme":
        return '<span class="badge-ok">Conforme</span>'
    if status == "Atenções":
        return '<span class="badge-attn">Atenções</span>'
    return '<span class="badge-crit">Crítico</span>'


def exportar_pdf_relatorio(dados: dict, texto_teste: str) -> Path:
    """
    Gera um relatório PDF simples com resultados.
    Saída: exports/relatorios/validacao_edital_YYYYMMDD_HHMM.pdf
    """
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
    from reportlab.lib import colors

    out_dir = ROOT_DIR / "exports" / "relatorios"
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    path = out_dir / f"validacao_edital_{ts}.pdf"

    doc = SimpleDocTemplate(str(path), pagesize=A4, rightMargin=36, leftMargin=36, topMargin=60, bottomMargin=36)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="H1", fontSize=16, leading=19, spaceAfter=10))
    styles.add(ParagraphStyle(name="H2", fontSize=12, leading=15, spaceAfter=8))
    styles.add(ParagraphStyle(name="Body", fontSize=10, leading=13))
    story = []

    logo = carregar_logo()
    if logo:
        buf = io.BytesIO()
        logo.save(buf, format="PNG")
        buf.seek(0)
        story.append(RLImage(buf, width=120, height=60))
        story.append(Spacer(1, 6))

    story.append(Paragraph("Relatório de Validação de Edital – SAAB 5.0", styles["H1"]))
    story.append(Paragraph(datetime.now().strftime("%d/%m/%Y %H:%M"), styles["Body"]))
    story.append(Spacer(1, 8))

    story.append(Paragraph(f"Tipo de contratação: <b>{dados['tipo'].title()}</b>", styles["Body"]))
    story.append(Paragraph(f"Score geral: <b>{dados['score']}</b>", styles["Body"]))
    story.append(Paragraph(f"Status: <b>{dados['status']}</b>", styles["Body"]))
    story.append(Spacer(1, 8))

    # Tabela de achados
    if dados["achados"]:
        table_data = [["Severidade", "Seção", "Mensagem", "Recomendação"]]
        for a in dados["achados"]:
            table_data.append([a["severidade"], a["secao"], a["mensagem"], a["recomendacao"]])
        tbl = Table(table_data, colWidths=[70, 90, 200, 180])
        tbl.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f0f0f0")),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]
            )
        )
        story.append(Paragraph("Achados:", styles["H2"]))
        story.append(tbl)
        story.append(Spacer(1, 8))
    else:
        story.append(Paragraph("Nenhum achado relevante. Documento em conformidade.", styles["Body"]))
        story.append(Spacer(1, 8))

    story.append(Paragraph("Observações:", styles["H2"]))
    story.append(Paragraph(dados.get("observacoes", "-"), styles["Body"]))
    story.append(Spacer(1, 8))

    # Opcional: trecho do texto analisado
    if texto_teste.strip():
        story.append(Paragraph("Amostra do conteúdo analisado:", styles["H2"]))
        preview = texto_teste.strip()[:1200].replace("\n", "<br/>")
        story.append(Paragraph(preview, styles["Body"]))

    doc.build(story)
    return path


# ----------------------------------------------------------
# UI / Página
# ----------------------------------------------------------
st.set_page_config(page_title="Validador de Editais – SAAB 5.0", layout="wide", page_icon="🧠")
aplicar_css_basico()

# Cabeçalho
cols = st.columns([0.15, 0.85])
with cols[0]:
    logo = carregar_logo()
    if logo:
        st.image(logo, width=110)
with cols[1]:
    st.title("Validador de Editais – SAAB 5.0")
    st.markdown(
        "Verifique a conformidade do edital com a **Lei nº 14.133/21** e diretrizes do TJSP. "
        "Cole abaixo o conteúdo (ou parte representativa) do edital e execute a validação."
    )

st.divider()

# Entradas
tipo = st.selectbox("Selecione o tipo de contratação:", ["Serviços", "Materiais", "Obras", "TI & Software", "Consultorias"], index=0)
modo = st.radio("Modo de exibição dos resultados:", ["Resumo", "Detalhado"], horizontal=True, index=0)

st.subheader("🖊️ Insira o conteúdo do edital para validação:")
texto = st.text_area(
    "Cole o conteúdo (ou parte) do edital", height=220, placeholder="Ex.: O presente edital tem por objeto ...",
    label_visibility="collapsed",
)

# Ações
col_run, col_pdf = st.columns([0.25, 0.75])
with col_run:
    executar = st.button("▶️ Executar validação")

resultados = None

if executar:
    with st.spinner("Executando validação..."):
        resultados = executar_validacao(tipo=tipo.lower(), modo=modo.lower(), texto=texto)

    # Painel de resultados
    st.subheader("📊 Resultados")
    c1, c2, c3 = st.columns([0.18, 0.18, 0.64])
    with c1:
        st.metric("Score geral", f"{resultados['score']}")
    with c2:
        st.markdown(f"**Status:** {badge_status(resultados['status'])}", unsafe_allow_html=True)
    with c3:
        st.caption(resultados.get("observacoes", ""))

    # Achados
    if resultados["achados"]:
        st.markdown("**Achados:**")
        if modo.lower() == "resumo":
            # agrupar por severidade
            crit = sum(1 for a in resultados["achados"] if a["severidade"].lower() == "crítico")
            med = sum(1 for a in resultados["achados"] if a["severidade"].lower() == "médio")
            bai = sum(1 for a in resultados["achados"] if a["severidade"].lower() == "baixo")
            st.write(
                f"- Críticos: **{crit}**  |  Médios: **{med}**  |  Baixos: **{bai}**"
            )
        else:
            import pandas as pd

            df = pd.DataFrame(resultados["achados"])
            st.dataframe(
                df[["severidade", "secao", "mensagem", "recomendacao"]],
                use_container_width=True,
                hide_index=True,
            )
    else:
        st.success("Nenhum achado relevante. Documento em conformidade.")

    # Exportar PDF
    with col_pdf:
        gerar = st.button("🧾 Exportar relatório em PDF")
        if gerar:
            with st.spinner("Gerando PDF institucional..."):
                pdf_path = exportar_pdf_relatorio(resultados, texto)
            st.success("Relatório gerado com sucesso.")
            st.download_button(
                "⬇️ Baixar relatório PDF",
                data=open(pdf_path, "rb").read(),
                file_name=pdf_path.name,
                mime="application/pdf",
            )

# Rodapé institucional
st.markdown("---")
st.caption("Projeto SAAB-Tech • Tribunal de Justiça de São Paulo • Secretaria de Administração e Abastecimento (SAAB)")
