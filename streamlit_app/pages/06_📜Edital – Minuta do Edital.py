# ==============================
# pages/06_📜Edital – Minuta do Edital.py  –  SynapseNext / SAAB TJSP
# ==============================

import streamlit as st
from datetime import datetime
import os, sys, json
from io import BytesIO
from docx import Document
from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
from openai import OpenAI
from pathlib import Path

# ==========================================================
# ⚙️ Configuração
# ==========================================================
st.set_page_config(page_title="📜 Edital – Minuta", layout="wide", page_icon="📜")
aplicar_estilo_global()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("openai_api_key")
client = OpenAI(api_key=OPENAI_API_KEY)

# ==========================================================
# 📚 Leitura de modelos da Knowledge Base
# ==========================================================
def ler_modelos_edital() -> str:
    base = Path(__file__).resolve().parents[1] / "knowledge" / "edital_models"
    textos = []
    if base.exists():
        for arq in base.glob("*.txt"):
            try:
                textos.append(arq.read_text(encoding="utf-8"))
            except Exception:
                pass
    return "\n\n".join(textos)

# ==========================================================
# 🏛️ Cabeçalho institucional
# ==========================================================
exibir_cabecalho_padrao(
    "📜 Minuta do Edital de Licitação",
    "Geração automatizada com IA institucional a partir dos artefatos TR, ETP e DFD"
)
st.divider()

# ==========================================================
# 🔗 Dados disponíveis na sessão
# ==========================================================
defaults = {}

for fonte in ["tr_campos_ai", "etp_campos_ai", "dfd_campos_ai"]:
    if fonte in st.session_state:
        defaults.update(st.session_state[fonte])

if defaults:
    st.success("📎 Dados recebidos automaticamente dos módulos anteriores (TR, ETP, DFD).")
else:
    st.info("Nenhum insumo ativo detectado. Você pode preencher manualmente ou aguardar integração via módulo **INSUMOS**.")

# ==========================================================
# 🧾 Formulário – Campos base do Edital
# ==========================================================
st.subheader("📘 Entrada – Dados da Minuta do Edital")

col1, col2 = st.columns(2)
with col1:
    unidade_solicitante = st.text_input("Unidade solicitante", value=defaults.get("unidade_solicitante", ""))
    responsavel_tecnico = st.text_input("Responsável técnico", value=defaults.get("responsavel_tecnico", ""))
    objeto = st.text_area("Objeto da licitação", value=defaults.get("objeto", ""), height=100)
    modalidade = st.text_input("Modalidade de licitação", value=defaults.get("modalidade", "Pregão Eletrônico"))
    regime_execucao = st.text_input("Regime de execução", value=defaults.get("regime_execucao", "Menor preço global"))
with col2:
    base_legal = st.text_input("Base legal", value=defaults.get("base_legal", "Lei nº 14.133/2021"))
    criterios_julgamento = st.text_area("Critérios de julgamento", value=defaults.get("criterios_julgamento", ""), height=100)
    prazo_execucao = st.text_input("Prazo de execução", value=defaults.get("prazo_execucao", ""))
    forma_pagamento = st.text_input("Forma de pagamento", value=defaults.get("forma_pagamento", "Conforme cronograma físico-financeiro"))
    penalidades = st.text_area("Penalidades e sanções", value=defaults.get("penalidades", ""), height=100)

observacoes_finais = st.text_area("Observações finais", value=defaults.get("observacoes_finais", ""), height=80)

# ==========================================================
# ⚙️ Geração do Artefato com IA
# ==========================================================
st.divider()
st.subheader("⚙️ Geração de Minuta com IA Institucional")

if st.button("🤖 Gerar minuta do Edital com IA institucional"):
    with st.spinner("Gerando minuta completa com base nos artefatos e modelos do TJSP..."):
        modelos = ler_modelos_edital()
        campos = {
            "unidade_solicitante": unidade_solicitante,
            "responsavel_tecnico": responsavel_tecnico,
            "objeto": objeto,
            "modalidade": modalidade,
            "regime_execucao": regime_execucao,
            "base_legal": base_legal,
            "criterios_julgamento": criterios_julgamento,
            "prazo_execucao": prazo_execucao,
            "forma_pagamento": forma_pagamento,
            "penalidades": penalidades,
            "observacoes_finais": observacoes_finais,
        }

        user_prompt = f"""
Com base nos campos abaixo e nos modelos institucionais da SAAB/TJSP,
elabore a minuta completa de um **Edital de Licitação**, seguindo o padrão redacional do TJSP.

Campos:
{json.dumps(campos, ensure_ascii=False, indent=2)}

Modelos de referência:
\"\"\"{modelos}\"\"\"
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Você é um redator institucional do Tribunal de Justiça de São Paulo, responsável por elaborar minutas de edital conforme os padrões da SAAB/TJSP e da Lei nº 14.133/2021."},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3
            )

            artefato_edital = response.choices[0].message.content.strip()
            st.session_state["artefato_edital_gerado"] = artefato_edital
            st.success("✅ Minuta gerada com sucesso! Você pode visualizar e exportar o documento.")

            st.text_area("📄 Pré-visualização da minuta gerada:", artefato_edital, height=400)

        except Exception as e:
            st.error(f"Erro ao gerar minuta com IA: {e}")

# ==========================================================
# 💾 Exportação do Artefato (DOCX)
# ==========================================================
if "artefato_edital_gerado" in st.session_state:
    artefato_edital = st.session_state["artefato_edital_gerado"]
    doc = Document()
    doc.add_heading("MINUTA DO EDITAL DE LICITAÇÃO", level=1)
    doc.add_paragraph(artefato_edital)

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    st.download_button(
        label="📤 Exportar minuta em DOCX",
        data=buffer,
        file_name="Edital_rascunho.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

st.caption("📎 O texto acima é gerado pela IA institucional com base nos modelos oficiais do TJSP e nos artefatos TR, ETP e DFD.")
