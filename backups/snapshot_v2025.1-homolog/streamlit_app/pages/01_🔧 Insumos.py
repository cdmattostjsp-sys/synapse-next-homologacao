import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# ==========================================================
# pages/01_🔧 Insumos.py
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# Revisão: Engenheiro Synapse – Versão 2025-D4 (Upload Fix)
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

# [CORREÇÃO CRÍTICA]: Removida a linha st.session_state.pop()
# A manipulação manual do state no topo do script causava race condition
# no Streamlit Cloud, resetando o arquivo enviado para None.

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

# Atualizei a chave para garantir um estado limpo nesta nova versão
uploaded_file = st.file_uploader(
    "Selecione o arquivo de insumo (formatos aceitos: TXT, DOCX, PDF)",
    type=["txt", "docx", "pdf"],
    key="insumo_upload_final"
)

# 🔍 BLOCO DEBUG (Pode remover após confirmar o funcionamento)
if uploaded_file is not None:
    st.info(f"✅ Arquivo carregado na memória: {uploaded_file.name} ({uploaded_file.size} bytes)")

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
    # Espaço visual para separar o botão
    st.write("")
    
    if st.button(f"🚀 Processar e encaminhar para {artefato}", key="btn_processar_insumo"):
        with st.spinner(f"Processando insumo para o módulo {artefato}..."):
            try:
                resultado = processar_insumo(uploaded_file, artefato)

                if resultado:
                    st.success(f"✅ Insumo processado com sucesso e integrado ao módulo {artefato}.")
                    st.toast(
                        "💾 Resultado armazenado em exports/insumos/json/",
                        icon="📁"
                    )

                    with st.expander("🔍 Detalhes do JSON Gerado", expanded=False):
                        st.json(resultado)

                else:
                    st.warning("⚠️ O processamento não retornou dados válidos. Verifique o conteúdo do arquivo.")
            except Exception as e:
                st.error(f"❌ Erro ao processar insumo: {e}")

else:
    st.info("👆 Selecione um arquivo acima para habilitar o processamento.")

# ==========================================================
# 🗒️ Histórico de insumos processados
# ==========================================================
st.divider()
st.subheader("📚 Histórico de insumos disponíveis")

EXPORTS_JSON_DIR = os.path.join("exports", "insumos", "json")

if os.path.exists(EXPORTS_JSON_DIR):
    arquivos = sorted(
        [f for f in os.listdir(EXPORTS_JSON_DIR) if f.endswith(".json")],
        reverse=True
    )

    if arquivos:
        st.caption(f"Últimos arquivos processados ({len(arquivos)} encontrados):")
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
    # Cria o diretório silenciosamente para evitar erro visual na próxima execução
    try:
        os.makedirs(EXPORTS_JSON_DIR, exist_ok=True)
        st.info("Diretório de exportação inicializado.")
    except:
        st.info("Nenhum histórico encontrado.")

# ==========================================================
# 🌟 Rodapé institucional
# ==========================================================
st.divider()
st.caption(
    "📎 Módulo de Insumos – SynapseNext (TJSP/SAAB). "
)
