# -*- coding: utf-8 -*-
# =============================================================================
# SynapseNext – SAAB/TJSP
# Página: DFD – Formalização da Demanda (vNext)
# =============================================================================

import streamlit as st
from pathlib import Path
import json
import sys
import os

# -------------------------------------------------------------------------
# 🧠 Path Resolver – compatível com Streamlit Cloud e Codespaces
# -------------------------------------------------------------------------
BASE_PATH = Path(__file__).resolve().parents[2]
UTILS_PATH = BASE_PATH / "streamlit_app" / "utils"

if str(UTILS_PATH) not in sys.path:
    sys.path.insert(0, str(UTILS_PATH))

# -------------------------------------------------------------------------
# 📦 Importações institucionais (com fallback seguro)
# -------------------------------------------------------------------------
try:
    from utils.agents_bridge import AgentsBridge
except ModuleNotFoundError:
    from streamlit_app.utils.agents_bridge import AgentsBridge

try:
    from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
except ModuleNotFoundError:
    aplicar_estilo_global = lambda: None
    exibir_cabecalho_padrao = lambda t: st.title(t)

# -------------------------------------------------------------------------
# 🧭 Configuração da página
# -------------------------------------------------------------------------
st.set_page_config(page_title="📄 DFD – Formalização da Demanda", layout="wide")
aplicar_estilo_global()
exibir_cabecalho_padrao("📄 DFD – Formalização da Demanda")

EXPORTS_DIR = BASE_PATH / "exports"
DFD_JSON_PATH = EXPORTS_DIR / "dfd_data.json"
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------------------
# 🧩 Etapa 1 – Formulário de Metadados
# -------------------------------------------------------------------------
st.markdown("### 🧩 Etapa 1 – Preenchimento dos Dados Institucionais")

with st.form("form_dfd"):
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Unidade Demandante", key="dfd_unidade", placeholder="Ex.: Secretaria de Administração e Abastecimento – SAAB")
        st.text_input("Responsável pela Demanda", key="dfd_responsavel")
        st.text_input("Prazo Estimado para Atendimento", key="dfd_prazo")
    with col2:
        st.text_area("Descrição da Necessidade", key="dfd_descricao", height=120)
        st.text_area("Motivação da Contratação", key="dfd_motivacao", height=120)
        st.number_input("Estimativa de Valor (R$)", key="dfd_estimativa_valor", min_value=0.0, step=1000.0)

    submitted = st.form_submit_button("💾 Salvar Dados")

if submitted:
    st.session_state["DFD_METADATA"] = {
        "unidade": st.session_state.get("dfd_unidade"),
        "descricao": st.session_state.get("dfd_descricao"),
        "motivacao": st.session_state.get("dfd_motivacao"),
        "prazo": st.session_state.get("dfd_prazo"),
        "estimativa_valor": st.session_state.get("dfd_estimativa_valor"),
        "responsavel": st.session_state.get("dfd_responsavel"),
    }
    st.success("✅ Dados do DFD armazenados na sessão.")

# -------------------------------------------------------------------------
# 🤖 Etapa 2 – Geração de Rascunho Inteligente (IA Institucional)
# -------------------------------------------------------------------------
st.divider()
st.markdown("### 🤖 Etapa 2 – Geração Automática com IA Institucional")

if st.button("⚙️ Gerar rascunho com IA (DFD)"):
    metadata = st.session_state.get("DFD_METADATA", {})
    if not metadata:
        st.warning("Por favor, preencha e salve o formulário antes de gerar o rascunho.")
    else:
        try:
            bridge = AgentsBridge("DFD")
            doc = bridge.generate(metadata)
            st.session_state["DFD_AI"] = doc
            st.success("Rascunho do DFD gerado com sucesso!")
            with st.expander("📄 Prévia do Rascunho (JSON)", expanded=False):
                st.json(doc)

            # salva o arquivo JSON institucional
            with open(DFD_JSON_PATH, "w", encoding="utf-8") as f:
                json.dump(doc, f, ensure_ascii=False, indent=2)
            st.info(f"💾 Arquivo salvo: {DFD_JSON_PATH.name}")

        except Exception as e:
            st.error(f"❌ Falha ao gerar rascunho com IA institucional: {e}")

# -------------------------------------------------------------------------
# 📤 Etapa 3 – Exportação
# -------------------------------------------------------------------------
st.divider()
st.markdown("### 📤 Etapa 3 – Exportar Documento")

if DFD_JSON_PATH.exists():
    with open(DFD_JSON_PATH, "rb") as f:
        st.download_button(
            label="📤 Exportar DFD (JSON)",
            data=f,
            file_name="dfd_data.json",
            mime="application/json"
        )
else:
    st.info("Nenhum rascunho foi gerado ainda.")

# -------------------------------------------------------------------------
# 🕒 Rodapé Institucional
# -------------------------------------------------------------------------
st.markdown("""
---
<p style='text-align:center;color:#666;font-size:0.9rem'>
DFD – Formalização da Demanda • SynapseNext vNext<br>
Secretaria de Administração e Abastecimento – SAAB/TJSP<br>
Ambiente validado em execução no Streamlit Cloud.
</p>
""", unsafe_allow_html=True)
