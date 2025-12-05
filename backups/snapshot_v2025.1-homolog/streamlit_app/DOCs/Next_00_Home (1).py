# streamlit_app/pages/Next_00_Home.py
# Capa institucional + navegação interna

import sys
from pathlib import Path

# Adiciona a raiz do repositório ao PYTHONPATH (necessário no Streamlit Cloud)
# .../synapse-next/streamlit_app/pages/Next_00_Home.py -> sobe 2 níveis
sys.path.append(str(Path(__file__).resolve().parents[2]))

import streamlit as st
from datetime import datetime

st.set_page_config(page_title="SynapseNext – Home", layout="wide")

# =========================
# Cabeçalho Institucional
# =========================
st.title("SynapseNext — Fase Brasília (Ecossistema SAAB 5.0)")
st.caption("Ambiente operacional para geração de artefatos da fase interna: **DFD → ETP → TR → Contrato**.")

col_a, col_b = st.columns([3, 2])
with col_a:
    st.markdown(
        """
### Objetivo
O **SynapseNext** padroniza a produção dos artefatos da fase interna de contratação, com:
- **Rascunho institucional** em Markdown;
- **Exportação** para `.docx` (e `.pdf` como opcional em passos futuros);
- **Validação semântica** (acoplada no Passo 2);
- **Rastreabilidade**, com logs mínimos e salvamento de rascunhos.
        """
    )
with col_b:
    st.markdown(
        """
### Diretrizes desta fase
- **UI**: Streamlit (layout *wide*), linguagem institucional, textos de ajuda.
- **Exportação**: `utils/formatter_docx.markdown_to_docx`.
- **Logs**: `exports/logs` e rascunhos em `exports/rascunhos`.
- **Sem** AJAX/JS externo. Somente Python/Streamlit.
        """
    )

st.divider()

# =========================
# Navegação interna
# =========================
st.subheader("Navegação")

nav_cols = st.columns(4)
destinos = {
    "DFD": "pages/Next_10_DFD.py",
    "ETP": None,     # Placeholder (próximos passos)
    "TR": None,      # Placeholder (próximos passos)
    "Contrato": None # Placeholder (próximos passos)
}

def _page_link_or_fallback(label: str, page_path: str | None):
    if page_path:
        try:
            st.page_link(page_path, label=label, icon="➡️")
        except Exception:
            if st.button(label):
                try:
                    st.switch_page(page_path)
                except Exception:
                    st.warning("Use o menu ‘Pages’ na barra lateral para abrir a página correspondente.")
    else:
        st.write(f"🔒 {label} *(disponível nos próximos passos)*")

with nav_cols[0]:
    _page_link_or_fallback("DFD – Documento de Formalização da Demanda", destinos["DFD"])
with nav_cols[1]:
    _page_link_or_fallback("ETP – Estudo Técnico Preliminar", destinos["ETP"])
with nav_cols[2]:
    _page_link_or_fallback("TR – Termo de Referência", destinos["TR"])
with nav_cols[3]:
    _page_link_or_fallback("Contrato", destinos["Contrato"])

st.divider()

# =========================
# Jornada e fluxo
# =========================
st.subheader("Jornada prevista")
st.markdown(
    """
1. **DFD** → Coletar informações essenciais e gerar **rascunho institucional** (Markdown) com **exportação `.docx`**.  
2. **ETP** → Encadear respostas do DFD e detalhar o estudo técnico preliminar.  
3. **TR** → Encadear dados do ETP para compor o termo de referência.  
4. **Contrato** → Encadear especificações do TR e consolidar o artefato final.

> **Validação semântica:** integrada no **Passo 2** via `validator_engine_vNext.validate_document`.
    """
)

# =========================
# Placeholders (sem integração)
# =========================
with st.expander("📎 Placeholders institucionais (futuro)"):
    st.markdown(
        """
- **SharePoint/OneDrive**: upload/download de artefatos (Passo 6).
- **Templates `.docx` institucionais** (opcional no Passo 7).
- **Modo com/sem sugestões** no `.docx` (Passo 3).
        """
    )

# =========================
# Verificação de diretórios de saída
# =========================
base = Path(__file__).resolve().parents[2]  # .../synapse-next
exports = base / "exports"
logs_dir = exports / "logs"
rascunhos_dir = exports / "rascunhos"
for p in (exports, logs_dir, rascunhos_dir):
    p.mkdir(parents=True, exist_ok=True)

st.info(
    f"📂 Diretórios de saída prontos: `{logs_dir.relative_to(base)}` e `{rascunhos_dir.relative_to(base)}`."
)
