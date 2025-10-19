import streamlit as st
from datetime import datetime

# =============================================================================
# Página: SynapseNext – Fase Brasília (Ecosistema SAAB 5.0)
# =============================================================================

st.set_page_config(page_title="SynapseNext – Fase Brasília", layout="wide")

# -----------------------------------------------------------------------------
# Cabeçalho
# -----------------------------------------------------------------------------
st.title("SynapseNext — Fase Brasília (Ecossistema SAAB 5.0)")
st.caption("Ambiente operacional para geração de artefatos da fase interna: **DFD → ETP → TR → Contrato.**")

# -----------------------------------------------------------------------------
# Bloco: Objetivo
# -----------------------------------------------------------------------------
st.header("Objetivo")

st.markdown("""
O **SynapseNext** padroniza a produção dos artefatos da fase interna de contratação, com:

- **Rascunho institucional** em formato Markdown;
- **Exportação** para `.docx` (e `.pdf` como opção em versões futuras);
- **Validação semântica** (acoplada no Passo 2);
- **Rastreabilidade**, com logs mínimos e salvamento automático de rascunhos.
""")

# -----------------------------------------------------------------------------
# Bloco: Diretrizes desta fase
# -----------------------------------------------------------------------------
st.header("Diretrizes desta fase")

st.markdown("""
- **UI:** baseada em *Streamlit* (layout `wide`), com linguagem institucional e orientações integradas.
- **Exportação:** `utils/formatter_docx.markdown_to_docx`.
- **Logs:** `exports/logs` e rascunhos em `exports/rascunhos`.
- **Sem** dependência de *JavaScript/AJAX* externo — apenas *Python/Streamlit* puro.
""")

# -----------------------------------------------------------------------------
# Bloco: Navegação
# -----------------------------------------------------------------------------
st.header("Navegação")

st.markdown("""
➡️ **DFD – Documento de Formalização da Demanda**

🔒 **ETP – Estudo Técnico Preliminar** *(disponível nos próximos passos)*

🔒 **TR – Termo de Referência** *(disponível nos próximos passos)*

🔒 **Contrato** *(disponível nos próximos passos)*
""")

# -----------------------------------------------------------------------------
# Bloco: Jornada prevista
# -----------------------------------------------------------------------------
st.header("Jornada prevista")

st.markdown("""
1. **DFD** → Coletar informações essenciais e gerar *rascunho institucional* (Markdown) com exportação `.docx`.
2. **ETP** → Encadear respostas do DFD e detalhar o estudo técnico preliminar.
3. **TR** → Encadear dados do ETP para compor o termo de referência.
4. **Contrato** → Encadear especificações do TR e consolidar o artefato final.

> A **validação semântica** está integrada no *Passo 2*, utilizando `validator_engine_vNext.validate_document`.
""")

# -----------------------------------------------------------------------------
# Bloco: Placeholders institucionais
# -----------------------------------------------------------------------------
with st.expander("⚙️ Placeholders institucionais (futuro)"):
    st.markdown("""
    - Parâmetros de integração com o agente **DFD.IA**.
    - Sugestões automáticas para **ETP.IA** e **TR.IA**.
    - Motor de recomendações e conexões contextuais com bases documentais institucionais.
    """)

# -----------------------------------------------------------------------------
# Bloco: Rodapé informativo
# -----------------------------------------------------------------------------
st.info(f"📂 Diretórios de saída prontos: `exports/logs` e `exports/rascunhos` (checados em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}).")

# -----------------------------------------------------------------------------
# Observação de desenvolvimento futuro
# -----------------------------------------------------------------------------
st.caption("💡 Módulo de recomendações será ativado nas próximas versões (vNext).")

