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
root_dir = Path(__file__).resolve().parents[2]
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

# Importa o estilo e rodapé institucional
from utils.ui_style import aplicar_estilo_institucional, rodape_institucional

VALIDADOR_BASICO_OK = True
try:
    from validators.edital_validator import validar_edital
    from knowledge.validators.edital_semantic_validator import validar_semantica_edital
except Exception:
    VALIDADOR_BASICO_OK = False


# ----------------------------------------------------------
# UI / Página
# ----------------------------------------------------------
st.set_page_config(page_title="Validador de Editais – SAAB 5.0", layout="wide", page_icon="🧩")
aplicar_estilo_institucional()

# ==========================================================
# 🏛️ Cabeçalho institucional (ajuste fino, padrão aprovado)
# ==========================================================
try:
    logo_path = root_dir / "assets" / "tjsp_logo.png"
    if logo_path.exists():
        logo = Image.open(logo_path)
        col_logo, col_titulo = st.columns([0.12, 0.88])
        with col_logo:
            st.image(logo, width=90)
        with col_titulo:
            st.markdown(
                """
                <div style="margin-top:-6px;">
                    <h1 style="font-size:1.8rem; margin-bottom:0;">Validador de Editais – SAAB 5.0</h1>
                    <p style="font-size:1.0rem; color:#555;">Verifique a conformidade do edital com a Lei nº 14.133/21 e normas do TJSP</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.warning(f"⚠️ Logo não encontrado em: {logo_path}")
except Exception as e:
    st.error(f"Erro ao carregar o cabeçalho: {e}")

st.divider()

# ==========================================================
# ⚙️ Interface de Validação
# ==========================================================
st.markdown("### 📑 Cole abaixo o texto (ou parte) do edital para análise:")
texto_edital = st.text_area("Conteúdo do edital", height=300, placeholder="Cole aqui o conteúdo do edital...")

col1, col2 = st.columns([0.5, 0.5])
with col1:
    tipo_contratacao = st.selectbox(
        "Tipo de contratação:",
        ["Serviços", "Aquisição de Materiais", "Obras e Engenharia", "Outros"],
    )
with col2:
    modo_validacao = st.selectbox(
        "Modo de validação:",
        ["Completo (estrutural + semântico)", "Somente estrutural", "Somente semântico"],
    )

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

        achados = checklist.get("achados", []) + semantica.get("achados", [])
        score_sem = semantica.get("score", 0)
        penalidade = sum(
            10 if a.get("severidade") == "Crítico"
            else 5 if a.get("severidade") == "Médio"
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

# ==========================================================
# 🚀 Execução da Validação
# ==========================================================
if st.button("🚀 Executar Validação", use_container_width=True):
    with st.spinner("Executando validação, por favor aguarde..."):
        resultado = executar_validacao(tipo_contratacao, modo_validacao, texto_edital)

    st.markdown("---")
    st.subheader("📊 Resultado da Análise")

    cor_status = (
        "✅ Conforme" if resultado["status"] == "Conforme"
        else "⚠️ Atenções" if resultado["status"] == "Atenções"
        else "❌ Crítico"
    )
    st.markdown(f"**Status Geral:** {cor_status}")
    st.progress(resultado["score"] / 100)
    st.write(f"**Score Geral:** {resultado['score']} / 100")

    st.markdown("#### 🧾 Detalhamento dos Achados")
    if resultado["achados"]:
        for a in resultado["achados"]:
            st.markdown(
                f"**{a['severidade']} – {a['secao']}**  \n"
                f"{a['mensagem']}  \n"
                f"💡 {a['recomendacao']}  \n"
                "---"
            )
    else:
        st.info("Nenhum problema identificado nas validações aplicadas.")

    st.markdown("#### 📌 Observações")
    st.write(resultado["observacoes"])

    buffer = io.BytesIO(str(resultado).encode("utf-8"))
    st.download_button(
        label="💾 Baixar Resultado (.txt)",
        data=buffer,
        file_name=f"resultado_validacao_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain",
    )

# ----------------------------------------------------------
# Rodapé institucional
# ----------------------------------------------------------
st.markdown("---")
rodape_institucional()
