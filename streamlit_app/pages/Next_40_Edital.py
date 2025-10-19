import streamlit as st
from datetime import datetime
from utils.next_pipeline import build_edital_markdown

st.set_page_config(page_title="Next 40 – Edital", layout="wide")

st.markdown("# 📘 Next 40 – Edital")
st.markdown("### Artefato final da Fase Interna da Licitação")

st.info(
    """
    O **Edital** é o documento que encerra a fase interna e dá início à fase externa da licitação.  
    Ele consolida as informações técnicas, jurídicas e orçamentárias reunidas nos artefatos anteriores:
    - DFD (necessidade e motivação)
    - ETP (análise de viabilidade)
    - TR (descrição técnica e critérios)
    """
)

# --- Coleta de dados simples para teste inicial ---
with st.form("form_edital"):
    objeto = st.text_area("📄 Descreva o objeto da licitação:")
    fundamento = st.text_area("⚖️ Fundamento legal (artigos, incisos, dispositivos):")
    criterios = st.text_area("📊 Critérios de julgamento (menor preço, técnica e preço, etc.):")
    clausulas = st.text_area("📑 Cláusulas essenciais (prazos, garantias, sanções):")
    submitted = st.form_submit_button("Gerar Rascunho do Edital")

if submitted:
    respostas = {
        "objeto": objeto,
        "fundamento": fundamento,
        "criterios": criterios,
        "clausulas": clausulas,
        "data": datetime.now().strftime("%d/%m/%Y"),
    }
    markdown = build_edital_markdown(respostas)
    st.download_button(
        "📥 Baixar Edital Gerado",
        data=markdown,
        file_name="Edital_SynapseNext.md",
        mime="text/markdown",
    )
    st.success("Rascunho gerado com sucesso!")
