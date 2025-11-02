# ==========================================================
# pages/01_🔧 Insumos.py
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# ==========================================================
# Página de gestão e envio de insumos administrativos
# Compatível com os módulos DFD, ETP, TR e Edital
# ==========================================================

import streamlit as st
import os
from datetime import datetime
from utils.integration_insumos import processar_insumo
from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao

# ==========================================================
# ⚙️ Configuração inicial
# ==========================================================
st.set_page_config(page_title="🔧 Insumos – Upload e Integração", layout="wide", page_icon="🧩")
aplicar_estilo_global()

exibir_cabecalho_padrao(
    "🔧 Módulo de Insumos",
    "Envie documentos administrativos para processamento e integração automatizada com os módulos DFD, ETP, TR e Edital."
)
st.divider()

# ==========================================================
# 📂 Interface de Upload
# ==========================================================
st.subheader("📎 Envio de documento administrativo")

uploaded_file = st.file_uploader(
    "Selecione o arquivo a ser processado (formatos aceitos: TXT, DOCX, PDF)",
    type=["txt", "docx", "pdf"]
)

# ==========================================================
# 🧭 Seleção do módulo de destino
# ==========================================================
artefato_opcoes = ["DFD", "ETP", "TR", "EDITAL"]
artefato = st.selectbox("Selecione o módulo de destino do insumo:", artefato_opcoes)

# ==========================================================
# 🚀 Botão de processamento
# ==========================================================
if uploaded_file and artefato:
    if st.button("🚀 Pré-preencher com IA e encaminhar"):
        with st.spinner(f"Processando insumo para o módulo {artefato}..."):
            try:
                resultado = processar_insumo(uploaded_file, artefato)
                if resultado:
                    st.success(f"✅ Insumo {artefato} processado e encaminhado com sucesso.")
                else:
                    st.warning("⚠️ O processamento não retornou dados válidos. Verifique o arquivo enviado.")
            except Exception as e:
                st.error(f"Erro ao processar insumo: {e}")
else:
    st.info("Envie um arquivo e selecione o módulo de destino para iniciar o processamento.")

# ==========================================================
# 🧾 Histórico de insumos processados
# ==========================================================
st.divider()
st.subheader("📚 Histórico de insumos disponíveis")

EXPORTS_JSON_DIR = os.path.join("exports", "insumos", "json")
if os.path.exists(EXPORTS_JSON_DIR):
    arquivos = sorted([f for f in os.listdir(EXPORTS_JSON_DIR) if f.endswith(".json")], reverse=True)
    if arquivos:
        for arquivo in arquivos[:5]:
            caminho = os.path.join(EXPORTS_JSON_DIR, arquivo)
            with open(caminho, "r", encoding="utf-8") as f:
                dados = f.read()
            with st.expander(f"🗂️ {arquivo}"):
                st.code(dados, language="json")
    else:
        st.info("Nenhum insumo processado ainda.")
else:
    st.info("Nenhum insumo processado ainda.")

# ==========================================================
# 🏁 Rodapé institucional
# ==========================================================
st.divider()
st.caption("📎 Módulo de Insumos – SynapseNext (TJSP/SAAB). Os insumos processados são automaticamente integrados aos módulos DFD, ETP, TR e Edital.")
