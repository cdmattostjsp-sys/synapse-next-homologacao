# ==========================================================
# pages/01_🔧 Insumos.py
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# Revisão: Engenheiro Synapse – Versão 2025-D3 + DEBUG
# ==========================================================

import os
import json
import streamlit as st
from pathlib import Path

# ==========================================================
# 📦 Imports institucionais (padrão unificado)
# ==========================================================
from utils.integration_insumos import processar_insumo
from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao

# ==========================================================
# ⚙️ Configuração inicial
# ==========================================================
st.set_page_config(
    page_title="🔧 Insumos – Upload e Integração",
    layout="wide",
    page_icon="🧩"
)

# Limpeza pontual de chave antiga que pode ter ficado em cache
st.session_state.pop("insumo_upload", None)

# Aplicar estilo e cabeçalho institucional
aplicar_estilo_global()
exibir_cabecalho_padrao(
    "🔧 Módulo de Insumos",
    "Envie documentos administrativos para processamento e integração automatizada "
    "com os módulos DFD, ETP, TR e Edital."
)
st.divider()

# ==========================================================
# 📂 Interface de Upload
# ==========================================================
st.subheader("📎 Envio de documento administrativo")

uploaded_file = st.file_uploader(
    "Selecione o arquivo de insumo (formatos aceitos: TXT, DOCX, PDF)",
    type=["txt", "docx", "pdf"],
    key="insumo_upload_v3"   # chave NOVA para quebrar qualquer cache antigo
)

# 🔍 BLOCO DEBUG – VISIBILIDADE DE BACKEND
with st.expander("🔍 DEBUG – Estado atual do uploader e sessão", expanded=False):
    st.write("uploaded_file é None?", uploaded_file is None)
    if uploaded_file is not None:
        st.write("Nome do arquivo:", uploaded_file.name)
        st.write("Tamanho em bytes (aprox.):", getattr(uploaded_file, "size", "N/D"))
    st.write("Chaves em st.session_state:", list(st.session_state.keys()))

# ==========================================================
# 🧭 Seleção do módulo de destino
# ==========================================================
artefato_opcoes = ["DFD", "ETP", "TR", "EDITAL"]
artefato = st.selectbox(
    "Selecione o módulo de destino do insumo:",
    artefato_opcoes,
    key="insumo_destino"
)

# ==========================================================
# 🚀 Processamento automático (com IA institucional)
# ==========================================================
if uploaded_file is not None:
    st.success(f"📄 Arquivo detectado: {uploaded_file.name}")

    if st.button(f"🚀 Processar e encaminhar para {artefato}", key="btn_processar_insumo"):
        with st.spinner(f"Processando insumo para o módulo {artefato}..."):
            try:
                resultado = processar_insumo(uploaded_file, artefato)

                if resultado:
                    st.success(f"✅ Insumo {artefato} processado com sucesso e integrado ao módulo {artefato}.")
                    st.toast(
                        "💾 Resultado armazenado em exports/insumos/json/ (ex: DFD_ultimo.json)",
                        icon="📁"
                    )

                    # DEBUG: mostrar payload resumido
                    with st.expander("🔍 DEBUG – Payload retornado por processar_insumo", expanded=False):
                        st.json(resultado)

                else:
                    st.warning("⚠️ O processamento não retornou dados válidos. Verifique o arquivo enviado.")
            except Exception as e:
                st.error(f"❌ Erro ao processar insumo: {e}")

else:
    st.info("Aguardando seleção de arquivo para iniciar o processamento.")

# ==========================================================
# 🗒️ Histórico de insumos processados
# ==========================================================
st.divider()
st.subheader("📚 Histórico de insumos disponíveis")

EXPORTS_JSON_DIR = os.path.join("exports", "insumos", "json")

st.caption(f"🔍 Diretório esperado de JSONs: `{EXPORTS_JSON_DIR}`")

if os.path.exists(EXPORTS_JSON_DIR):
    arquivos = sorted(
        [f for f in os.listdir(EXPORTS_JSON_DIR) if f.endswith(".json")],
        reverse=True
    )

    st.caption(f"Encontrados {len(arquivos)} arquivo(s) JSON neste diretório.")

    if arquivos:
        for arquivo in arquivos[:5]:
            caminho = os.path.join(EXPORTS_JSON_DIR, arquivo)
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                with st.expander(f"🗂️ {arquivo}"):
                    st.json(dados)
            except Exception:
                st.warning(f"⚠️ Não foi possível ler o arquivo {arquivo}.")
    else:
        st.info("Nenhum insumo processado ainda.")
else:
    st.info("Nenhum insumo processado ainda (diretório não existe).")

# ==========================================================
# 🌟 Rodapé institucional
# ==========================================================
st.divider()
st.caption(
    "📎 Módulo de Insumos – SynapseNext (TJSP/SAAB). "
    "Os insumos processados são automaticamente integrados aos módulos DFD, ETP, TR e Edital."
)
