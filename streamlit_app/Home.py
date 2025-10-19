import streamlit as st
import os
from datetime import datetime

# ============================
# CONFIGURAÇÕES INICIAIS
# ============================

st.set_page_config(
    page_title="SynapseNext — Hub",
    page_icon="⚖️",
    layout="wide",
)

# ============================
# CABEÇALHO COM LOGO TJSP
# ============================

# Caminho do logo institucional
logo_path = os.path.join("assets", "tjsp_logo.png")

# Layout do cabeçalho: logo + título
col1, col2 = st.columns([1, 6])
with col1:
    if os.path.exists(logo_path):
        st.image(logo_path, width=130)
with col2:
    st.markdown(
        """
        <div style='padding-top: 15px;'>
            <h1 style="font-size: 2.4rem; margin-bottom: 0;">SynapseNext — Hub</h1>
            <h5 style="color: #666; margin-top: 2px;">Ecosistema SAAB 5.0 • POC SynapseNext (Fase Brasília)</h5>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# ============================
# SEÇÃO “SOBRE”
# ============================

st.subheader("📘 Sobre")
st.markdown(
    """
    Este aplicativo consolida as páginas do **SynapseNext** para a fase interna  
    dos artefatos de contratação (**DFD → ETP → TR → Contrato**).

    Use o menu **Pages** (barra lateral) ou os atalhos abaixo.
    """
)

# ============================
# VERIFICAÇÃO DE DIRETÓRIOS
# ============================

logs_dir = "exports/logs"
drafts_dir = "exports/rascunhos"

# Garante que os diretórios existam
os.makedirs(logs_dir, exist_ok=True)
os.makedirs(drafts_dir, exist_ok=True)

# Verifica a data e hora da checagem
timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

st.success(
    f"📁 Pastas prontas: `{logs_dir}` e `{drafts_dir}` "
    f"(checadas em {timestamp})."
)

st.divider()

# ============================
# ATALHOS DE NAVEGAÇÃO
# ============================

st.subheader("🧭 Atalhos")
col1, col2 = st.columns(2)

with col1:
    st.page_link(
        "pages/Next_00_Home.py",
        label="➡️ Next 00 Home (Capa do SynapseNext)",
        icon="🏠",
    )

with col2:
    st.page_link(
        "pages/Next_10_DFD.py",
        label="➡️ Next 10 DFD (Form → Markdown → Docx → Validação)",
        icon="📄",
    )

st.info("💡 Dica: use o menu lateral para navegar entre as páginas.")

st.divider()

# ============================
# RODAPÉ INSTITUCIONAL
# ============================

st.markdown(
    """
    ---
    <div style='text-align: center; color: gray; font-size: 0.9em;'>
        Tribunal de Justiça do Estado de São Paulo — Secretaria de Administração e Abastecimento (SAAB)<br>
        Projeto Synapse.IA — Fase Brasília • Versão 5.0 (POC)
    </div>
    """,
    unsafe_allow_html=True
)
