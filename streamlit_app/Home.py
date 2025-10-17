import streamlit as st
from datetime import datetime

# ============================
# CONFIGURAÇÃO GERAL
# ============================

st.set_page_config(
    page_title="SynapseNext – Ecossistema SAAB 5.0",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================
# CABEÇALHO E IDENTIDADE
# ============================

st.title("🏛️ SynapseNext – Ecossistema SAAB 5.0")
st.caption("Ambiente integrado de apoio à Fase Interna das Contratações Públicas • SAAB/TJSP")

st.divider()

# ============================
# PAINEL DE INTRODUÇÃO
# ============================

st.subheader("🧭 Bem-vindo ao SynapseNext")
st.markdown(
    """
O **SynapseNext** é um ambiente de trabalho desenvolvido pela **Secretaria de Administração e Abastecimento (SAAB)** do **Tribunal de Justiça de São Paulo (TJSP)**, com o objetivo de 
**integrar, automatizar e validar os artefatos da fase interna das contratações públicas**, conforme a **Lei nº 14.133/2021** e a **IN SAAB nº 12/2025**.

Use o menu lateral ou as abas abaixo para navegar entre os módulos principais da jornada:

> 🧩 **DFD → ETP → TR → Contrato → Fiscalização**
"""
)

st.info(
    """
💡 **Dica:** Você pode importar arquivos PDF, DOCX ou relatórios técnicos para subsidiar a geração dos artefatos.  
O sistema analisará automaticamente o conteúdo e sugerirá aprimoramentos.
"""
)

st.divider()

# ============================
# SEÇÃO DE ACESSO RÁPIDO
# ============================

st.subheader("🚀 Acesso Rápido aos Módulos")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📘 Formalização da Demanda (DFD)")
    st.write("Crie o Documento de Formalização da Demanda com tutoria guiada e validação semântica.")
    st.page_link("pages/1_SynapseNext.py", label="Abrir DFD", icon="📘")

with col2:
    st.markdown("### 🧩 Estudo Técnico Preliminar (ETP)")
    st.write("Registre e compare alternativas técnicas, critérios de seleção e justificativas.")
    st.page_link("pages/1_SynapseNext.py", label="Abrir ETP", icon="🧩")

with col3:
    st.markdown("### 📑 Termo de Referência (TR)")
    st.write("Monte o TR com base nas informações do DFD e ETP, incluindo estimativas e critérios.")
    st.page_link("pages/1_SynapseNext.py", label="Abrir TR", icon="📑")

st.divider()

# ============================
# UPLOAD DE ARQUIVOS
# ============================

st.subheader("📎 Enviar Documentos de Apoio")

uploaded_files = st.file_uploader(
    "Selecione arquivos PDF, DOCX ou ZIP contendo informações da demanda:",
    accept_multiple_files=True,
    type=["pdf", "docx", "zip"],
)

if uploaded_files:
    st.success(f"{len(uploaded_files)} arquivo(s) carregado(s) com sucesso.")
    for file in uploaded_files:
        st.write(f"📄 {file.name}")

    st.info("🧠 Os documentos serão analisados automaticamente para extração de informações relevantes.")
else:
    st.caption("Nenhum arquivo enviado ainda.")

st.divider()

# ============================
# STATUS DO PROJETO
# ============================

st.subheader("📊 Status do Projeto")
st.markdown(
    f"""
**Versão:** `v1.0 – Estrutura de Abas Integradas`  
**Data:** {datetime.now().strftime("%d/%m/%Y")}  
**Desenvolvimento:** Equipe SAAB-8 • TJSP  
**Coordenação:** Carlos Darwin de Mattos  
**Arquitetura:** GPT-5 (OpenAI)  
"""
)

st.divider()
st.caption("SynapseNext • SAAB/TJSP – Prova de Conceito (Fase Brasília)")
