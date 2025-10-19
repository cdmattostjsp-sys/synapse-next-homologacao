import streamlit as st
from datetime import datetime
from PIL import Image
import os

# Caminho do logo
logo_path = os.path.join("assets", "tjsp_logo.png")

# --- Cabeçalho com logotipo ---
col1, col2 = st.columns([1, 8])
with col1:
    st.image(logo_path, width=180)
with col2:
    st.markdown(
        """
        # **SynapseNext — Hub**
        ### Ecossistema SAAB 5.0 • POC SynapseNext (Fase Brasília)
        """,
        unsafe_allow_html=True
    )

st.divider()

# --- Conteúdo principal ---
st.markdown("## 🧭 Estrutura de Artefatos da Fase Interna da Licitação")

st.markdown(
    """
    O SynapseNext organiza os **artefatos da Fase Interna da Licitação** conforme a Lei nº 14.133/2021.  
    Cada módulo corresponde a uma etapa lógica do processo de contratação, até a publicação do edital.
    """
)

st.markdown(
    """
    **Fluxo da Fase Interna:**
    1️⃣ **DFD** – Documento de Formalização da Demanda  
    2️⃣ **ETP** – Estudo Técnico Preliminar  
    3️⃣ **TR** – Termo de Referência / Projeto Básico  
    4️⃣ **EDITAL** – Consolidação e publicação das condições da licitação  
    ---
    Após o Edital, inicia-se a **Fase Externa**, composta por:
    - Julgamento
    - Adjudicação
    - Homologação
    - **Contrato**
    """
)

st.info("📂 Estrutura atualizada em: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

st.success(
    "Pastas de exportação: `exports/logs` e `exports/rascunhos` (checadas automaticamente)."
)

st.divider()
st.caption("Versão institucional SynapseNext • TJSP • Fase Brasília – Outubro/2025")
