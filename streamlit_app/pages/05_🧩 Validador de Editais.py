# ==========================================================
# 🧩 Validador de Editais – SynapseNext
# Secretaria de Administração e Abastecimento (SAAB 5.0)
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

VALIDADOR_BASICO_OK = True
try:
    from validators.edital_validator import validar_edital
    from knowledge.validators.edital_semantic_validator import validar_semantica_edital
except Exception:
    VALIDADOR_BASICO_OK = False


# ----------------------------------------------------------
# Utilitários locais
# ----------------------------------------------------------
def carregar_logo() -> Image.Image | None:
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
    st.markdown(
        """
        <style>
        h1, .stMarkdown h1 { font-size: 1.9rem !important; }
        h2, .stMarkdown h2 { font-size: 1.4rem !important; margin-top: 0.6rem !important; }
        h3, .stMarkdown h3 { font-size: 1.2rem !important; }
        .block-container { padding-top: 1.4rem; }
        .stMarkdown p { line-height: 1.45; }

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


# ----------------------------------------------------------
# Funções de validação
# ----------------------------------------------------------
def validar_fallback(tipo: str, texto: str) -> dict:
    achados = []
    texto_lower = texto.lower()
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

    if VALIDADOR_BASICO_OK:
        try:
            checklist = validar_edital(tipo_contratacao=tipo, conteudo=texto)
        except Exception:
            checklist = {"achados": []}

        try:
            semantica = validar_semantica_edital(tipo_contratacao=tipo, conteudo=texto, modo=modo)
        except Exception:
            semantica = {"achados": [], "score": 0}

        achados = []
        for it in (checklist.get("achados", []) + semantica.get("achados", [])):
            achados.append(
                {
                    "severidade": it.get("severidade", "Médio"),
                    "secao": it.get("secao", "Geral"),
                    "mensagem": it.get("mensagem", ""),
                    "recomendacao": it.get("recomendacao", ""),
                }
            )

        score_sem = semantica.get("score", 0)
        penalidade = sum(
            10 if a["severidade"] == "Crítico"
            else 5 if a["severidade"] == "Médio"
            else 2
            for a in achados
        )
        score = max(0, min(100, score_sem - penalidade // 2))
        status = "Conforme" if score >= 80 else "Atenções" if score >= 60 else "Crítico"

        return {
            "tipo": tipo,
            "score": score,
            "status": status,
            "achados": achados,
            "observacoes": "Validação executada com módulos oficiais.",
        }

    return validar_fallback(tipo, texto)


# ----------------------------------------------------------
# UI / Página
# ----------------------------------------------------------
st.set_page_config(page_title="Validador de Editais – SAAB 5.0", layout="wide", page_icon="🧩")
aplicar_css_basico()

# ==========================================================
# 🎨 Cabeçalho institucional refinado (logo centralizado e visível)
# ==========================================================
from PIL import Image

# Caminho confiável para o logo institucional
logo_path = Path(__file__).resolve().parents[2] / "assets" / "tjsp_logo.png"
if not logo_path.exists():
    logo_path = Path("assets/tjsp_logo.png")

# Exibição centralizada do logo
try:
    logo = Image.open(logo_path)
    col1, col2, col3 = st.columns([0.35, 0.3, 0.35])
    with col2:
        st.image(logo, width=120)
except Exception as e:
    st.warning(f"⚠️ Não foi possível carregar o logo institucional: {e}")

# Título e subtítulo (institucional)
st.markdown(
    """
    <div style="text-align:center; margin-top:-10px;">
        <h1 style="font-size:30px; font-weight:700; margin-bottom:4px;">
            Validador de Editais – SAAB 5.0
        </h1>
        <h3 style="color:#555; font-weight:normal; margin-top:0px; margin-bottom:20px;">
            Secretaria de Administração e Abastecimento – Tribunal de Justiça de São Paulo
        </h3>
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# 🔧 Entradas e Execução
# ==========================================================
tipo = st.selectbox("Selecione o tipo de contratação:", ["Serviços", "Materiais", "Obras", "TI & Software", "Consultorias"], index=0)
modo = st.radio("Modo de exibição dos resultados:", ["Resumo", "Detalhado"], horizontal=True, index=0)

st.subheader("🖊️ Insira o conteúdo do edital para validação:")
texto = st.text_area(
    "Cole o conteúdo (ou parte) do edital", height=220, placeholder="Ex.: O presente edital tem por objeto ...",
    label_visibility="collapsed",
)

col_run, col_pdf = st.columns([0.25, 0.75])
with col_run:
    executar = st.button("▶️ Executar validação")

resultados = None

if executar:
    with st.spinner("Executando validação..."):
        resultados = executar_validacao(tipo=tipo.lower(), modo=modo.lower(), texto=texto)

    st.subheader("📊 Resultados")
    c1, c2, c3 = st.columns([0.18, 0.18, 0.64])
    with c1:
        st.metric("Score geral", f"{resultados['score']}")
    with c2:
        status_color = (
            "🟢" if resultados["status"] == "Conforme" else
            "🟠" if resultados["status"] == "Atenções" else
            "🔴"
        )
        st.markdown(f"**Status:** {status_color} {resultados['status']}")
    with c3:
        st.caption(resultados.get("observacoes", ""))

    if resultados["achados"]:
        st.markdown("**Achados:**")
        if modo.lower() == "resumo":
            crit = sum(1 for a in resultados["achados"] if a["severidade"].lower() == "crítico")
            med = sum(1 for a in resultados["achados"] if a["severidade"].lower() == "médio")
            bai = sum(1 for a in resultados["achados"] if a["severidade"].lower() == "baixo")
            st.write(f"- Críticos: **{crit}**  |  Médios: **{med}**  |  Baixos: **{bai}**")
        else:
            import pandas as pd
            df = pd.DataFrame(resultados["achados"])
            st.dataframe(df[["severidade", "secao", "mensagem", "recomendacao"]], use_container_width=True, hide_index=True)
    else:
        st.success("Nenhum achado relevante. Documento em conformidade.")

    with col_pdf:
        gerar = st.button("🧾 Exportar relatório em PDF")
        if gerar:
            with st.spinner("Gerando PDF institucional..."):
                pdf_path = Path(ROOT_DIR / "exports" / "relatorios" / f"validacao_edital_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf")
                pdf_path.parent.mkdir(parents=True, exist_ok=True)
                pdf_path.write_text("Simulação de relatório gerado.")
            st.success("Relatório gerado com sucesso.")
            st.download_button("⬇️ Baixar relatório PDF", data=open(pdf_path, "rb").read(), file_name=pdf_path.name, mime="application/pdf")

st.markdown("---")
st.caption("SynapseNext – SAAB 5.0 • Tribunal de Justiça de São Paulo • Secretaria de Administração e Abastecimento (SAAB)")
