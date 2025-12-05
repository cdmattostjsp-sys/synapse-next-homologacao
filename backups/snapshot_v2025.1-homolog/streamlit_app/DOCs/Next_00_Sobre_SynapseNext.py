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
/utils/ → pipelines de auditoria, validação e formatação
/pages/ → interfaces de cada módulo (DFD, ETP, TR, Contrato, etc.)
/exports/ → repositório de saídas institucionais
├── analises/ → relatórios de coerência e KPIs (JSON)
├── relatorios/ → PDFs executivos e relatórios consolidados
├── auditoria/ → logs de trilha e histórico de revisões
├── rascunhos/ → versões intermediárias dos artefatos
└── logs/ → registros operacionais e alertas do sistema
/assets/ → logotipos, ícones e elementos visuais
/docs/ → documentação institucional e técnica (sem exibição pública)


O sistema não depende de bibliotecas externas de front-end (JavaScript, AJAX ou frameworks SPA), mantendo a **segurança compatível com o ambiente institucional TJSP**.
---
""")

# --------------------------------------------------------------
# Benefícios e diretrizes institucionais
# --------------------------------------------------------------
st.markdown("""
### 🏛️ Benefícios Institucionais

- **Padronização documental** e rastreabilidade integral das versões.  
- **Automação** e encadeamento entre artefatos (DFD → ETP → TR → Contrato).  
- **Validação semântica** acoplada à IA institucional do Synapse.  
- **Exportação integrada** para `.docx` e `.pdf`.  
- **Trilhas de auditoria e logs** com salvamento automático.  
- **Relatórios executivos** automatizados e padronizados para análise gerencial.  
- **Governança de dados** e transparência, em conformidade com o CNJ e a LGPD.

---
""")

# --------------------------------------------------------------
# Rodapé
# --------------------------------------------------------------
st.markdown("""
<div style="text-align:center; color:#666; font-size:0.9rem; margin-top:20px;">
TJSP • Secretaria de Administração e Abastecimento • Projeto SynapseNext – SAAB 5.0<br>
Versão institucional vNext (POC) • Desenvolvido em ambiente Python / Streamlit
</div>
""", unsafe_allow_html=True)

