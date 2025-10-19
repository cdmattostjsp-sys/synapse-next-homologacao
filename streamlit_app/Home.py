# streamlit_app/Home.py
# Hub inicial do SynapseNext: navegação para as páginas Next_* e informações do app.

import streamlit as st
from pathlib import Path
from datetime import datetime

# Configuração básica de página
st.set_page_config(page_title="SynapseNext – Hub", layout="wide")

st.title("SynapseNext — Hub")
st.caption("Ecossistema SAAB 5.0 • POC SynapseNext (Fase Brasília)")

col1, col2 = st.columns([3, 2], vertical_alignment="top")
with col1:
    st.markdown(
        """
### Sobre
Este aplicativo consolida as páginas do **SynapseNext** para a fase interna (DFD → ETP → TR → Contrato).

Use o menu **Pages** (barra lateral) ou os atalhos abaixo.
        """
    )
with col2:
    base = Path(__file__).resolve().parents[1]
    exports = base / "exports"
    (exports / "logs").mkdir(parents=True, exist_ok=True)
    (exports / "rascunhos").mkdir(parents=True, exist_ok=True)
    st.success(
        f"📂 Pastas prontas: `exports/logs` e `exports/rascunhos` "
        f"(checadas em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')})."
    )

st.divider()
st.subheader("Atalhos")

# Preferimos st.page_link (Streamlit novo). Mantemos fallback via botão.
def _link(label: str, path: str | None):
    if path:
        try:
            st.page_link(path, label=label, icon="➡️")
        except Exception:
            if st.button(label):
                try:
                    st.switch_page(path)
                except Exception:
                    st.warning("Abra pelo menu ‘Pages’ na barra lateral.")

cols = st.columns(2)
with cols[0]:
    _link("➡️ Next 00 Home (Capa do SynapseNext)", "pages/Next_00_Home.py")
with cols[1]:
    _link("➡️ Next 10 DFD (Form → Markdown → Docx → Validação)", "pages/Next_10_DFD.py")

st.info("Dica: use o menu **Pages** à esquerda para navegar entre as páginas.")
