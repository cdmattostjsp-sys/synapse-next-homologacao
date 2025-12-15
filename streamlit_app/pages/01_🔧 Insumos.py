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
from home_utils.sidebar_organizer import apply_sidebar_grouping
from home_utils.sidebar_organizer import apply_sidebar_grouping

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

# Aplicar CSS da sidebar
apply_sidebar_grouping()

# Estilo institucional PJe-inspired
st.markdown("""
<style>
/* ============================================
   PADRÃO VISUAL PJe-INSPIRED - SYNAPSE NEXT
   Versão: 2025.1-homolog
   Build: 20251215-1710
   ============================================ */

/* Título principal - tamanho reduzido para sobriedade */
h1 {
    font-size: 1.8rem !important;
    font-weight: 500 !important;
    color: #2c3e50 !important;
    margin-bottom: 0.3rem !important;
}

/* Caption institucional */
.caption {
    color: #6c757d;
    font-size: 0.9rem;
    margin-bottom: 1rem;
}

/* Seções com fundo cinza - contraste melhorado */
h2, h3 {
    font-size: 1.1rem !important;
    font-weight: 500 !important;
    color: #374151 !important;
    background-color: #e5e7eb !important;
    padding: 0.6rem 0.8rem !important;
    border-radius: 3px !important;
    margin-top: 1.5rem !important;
    margin-bottom: 1rem !important;
}

/* Botões - destaque apenas para ações principais */
div.stButton > button {
    border-radius: 3px;
    font-weight: 500;
    border: 1px solid #d0d7de;
}
div.stButton > button[kind="primary"] {
    background-color: #0969da !important;
    border-color: #0969da !important;
}

/* Formulário clean */
.stTextInput label, .stTextArea label, .stSelectbox label {
    font-weight: 500;
    color: #1f2937;
    font-size: 0.9rem;
}

/* Expander com destaque discreto */
details {
    border: 1px solid #d0d7de;
    border-radius: 3px;
    padding: 0.5rem;
    background-color: #ffffff;
}
summary {
    font-weight: 500;
    color: #0969da;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

# Cabeçalho institucional
st.markdown("<h1>🔧 Módulo de Insumos</h1>", unsafe_allow_html=True)
st.markdown("<p class='caption'>Envie documentos administrativos para processamento e integração automatizada com os módulos DFD, ETP, TR, Edital e Contrato</p>", unsafe_allow_html=True)
st.divider()

# ==========================================================
# 📂 Interface de Upload
# ==========================================================
st.markdown("### 📎 Envio de documento administrativo")

# Diagnóstico: Verificar se há conflitos no session_state
if 'debug_upload' not in st.session_state:
    st.session_state['debug_upload'] = True

# Atualizei a chave para garantir um estado limpo nesta nova versão
try:
    uploaded_file = st.file_uploader(
        "Selecione o arquivo de insumo (formatos aceitos: TXT, DOCX, PDF)",
        type=["txt", "docx", "pdf"],
        key="insumo_upload_final",
        help="💡 Dica: Se o upload não funcionar, tente recarregar a página (F5)"
    )
except Exception as e:
    st.error(f"❌ Erro no componente de upload: {e}")
    st.info("🔄 Tente recarregar a página (F5) ou limpar o cache do navegador")
    uploaded_file = None

# 🔍 BLOCO DEBUG (Pode remover após confirmar o funcionamento)
if uploaded_file is not None:
    st.success(f"✅ Arquivo carregado: **{uploaded_file.name}** ({uploaded_file.size:,} bytes)")
elif uploaded_file is False:
    st.error("❌ Erro ao carregar arquivo. Tente novamente.")
else:
    st.info("👆 Aguardando seleção de arquivo...")

# ==========================================================
# 🧭 Seleção do módulo de destino
# ==========================================================
col_select, col_reset = st.columns([4, 1])

with col_select:
    artefato_opcoes = ["DFD", "ETP", "TR", "EDITAL", "CONTRATO"]
    artefato = st.selectbox(
        "Selecione o módulo de destino do insumo:",
        artefato_opcoes,
        key="insumo_destino"
    )

with col_reset:
    st.write("")  # Espaçamento
    if st.button("🔄 Reset", help="Limpar estado e recarregar"):
        # Limpar chaves problemáticas do session_state
        keys_to_clear = [k for k in st.session_state.keys() if 'upload' in k.lower() or 'insumo' in k.lower()]
        for key in keys_to_clear:
            del st.session_state[key]
        st.rerun()

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
st.markdown("### 📚 Histórico de insumos disponíveis")

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
