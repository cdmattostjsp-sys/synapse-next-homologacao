# ==============================================================
# Documento Institucional: Sobre o SynapseNext – SAAB 5.0
# ==============================================================
# Finalidade:
# Documentar a visão, arquitetura e componentes do ecossistema
# SynapseNext, durante a fase de POC (Prova de Conceito).
# ==============================================================
import streamlit as st

st.set_page_config(
    page_title="Sobre o SynapseNext – SAAB 5.0",
    layout="wide",
    page_icon="ℹ️"
)

# --------------------------------------------------------------
# Cabeçalho
# --------------------------------------------------------------
st.markdown("""
## ℹ️ Sobre o SynapseNext – SAAB 5.0
O **SynapseNext** é o ecossistema digital da **Secretaria de Administração e Abastecimento (SAAB)** do Tribunal de Justiça de São Paulo, 
desenvolvido para apoiar, automatizar e auditar a **fase interna da licitação**, em conformidade com a **Lei nº 14.133/2021**, 
as **Resoluções do CNJ nº 651 e 652/2024**, e a **Instrução Normativa nº 12/2025** do TJSP.

Esta versão integra o ambiente de Prova de Conceito (POC), com arquitetura modular e foco em padronização institucional e transparência.
---
""")

# --------------------------------------------------------------
# Estrutura e componentes principais
# --------------------------------------------------------------
st.markdown("""
### 🧩 Estrutura do Ecossistema
O SynapseNext reflete o fluxo lógico da **fase interna da contratação pública**, composto pelos seguintes módulos:

1. **DFD – Documento de Formalização da Demanda**  
   Coleta informações iniciais e gera rascunho institucional.

2. **ETP – Estudo Técnico Preliminar**  
   Analisa viabilidade, alternativas e requisitos técnicos.

3. **TR – Termo de Referência**  
   Define objeto, critérios de medição e obrigações contratuais.

4. **Contrato**  
   Consolida as especificações e gera o instrumento final.

5. **Governança e Relatórios**  
   Reúnem indicadores de coerência, alertas proativos e relatórios executivos em PDF.
---
""")

# --------------------------------------------------------------
# Arquitetura técnica
# --------------------------------------------------------------
st.markdown("""
### ⚙️ Arquitetura Técnica
O ecossistema é desenvolvido em **Python + Streamlit**, com base em modularidade e rastreabilidade institucional.

**Estrutura de diretórios principal:**
