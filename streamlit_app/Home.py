# ==========================================================
# 🏠 SynapseNext – Página Inicial (Home)
# Secretaria de Administração e Abastecimento (SAAB 5.0)
# ==========================================================

import streamlit as st
from datetime import datetime
from pathlib import Path

# ==========================================================
# ⚙️ Configuração inicial
# ==========================================================
st.set_page_config(
    page_title="SynapseNext – SAAB 5.0",
    layout="wide",
    page_icon="🏛️"
)

# ==========================================================
# 🎨 Estilos institucionais
# ==========================================================
st.markdown("""
<style>
/* Fonte e hierarquia */
h1, h2, h3, h4 {
    font-family: 'Segoe UI', sans-serif;
    color: #444;
}
h1 {
    font-size: 1.6rem !important;
    margin-bottom: 0.6rem;
}
h2 {
    font-size: 1.2rem !important;
    color: #555;
}
h3 {
    font-size: 1.1rem !important;
    color: #666;
}
p, li {
    font-size: 0.95rem !important;
    color: #444;
    line-height: 1.5rem;
}

/* Layout */
.main {
    padding-top: 0rem;
}
hr {
    border: 0;
    height: 1px;
    background: #ddd;
    margin: 1.5rem 0;
}

/* Rodapé */
.footer {
    text-align: center;
    color: gray;
    font-size: 0.85rem;
    margin-top: 3rem;
    padding-top: 0.5rem;
    border-top: 1px solid #ddd;
}

/* Logotipo */
.logo-container {
    display: flex;
    align-items: center;
    gap: 12px;
}
.logo-container img {
    height: 42px;
    margin-top: -4px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# 🏛️ Cabeçalho institucional
# ==========================================================
logo_path = Path(__file__).resolve().parents[1] / "assets" / "tjsp_logo.png"
col1, col2 = st.columns([0.1, 1])
with col1:
    if logo_path.exists():
        st.image(str(logo_path))
with col2:
    st.markdown("""
    <div class="logo-container">
        <h1>SynapseNext – SAAB 5.0</h1>
    </div>
    <h2>Ambiente Institucional de Automação da Fase Interna de Licitação</h2>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ==========================================================
# 🧭 Corpo principal
# ==========================================================
st.markdown("""
O **SynapseNext** é um ecossistema digital desenvolvido pela
**Secretaria de Administração e Abastecimento (SAAB)** do Tribunal de Justiça de São Paulo,
destinado a padronizar, auditar e integrar os artefatos que compõem a **fase interna da licitação**,
de forma automatizada, transparente e aderente à **Lei nº 14.133/2021**.

Ele conecta módulos inteligentes e pipelines de governança que abrangem todo o ciclo de elaboração:
**DFD → ETP → TR → Edital → Contrato**.

---
### 🧩 Funcionalidades Principais
- **Criação orientada** de artefatos da fase interna (DFD, ETP, TR, Edital e Contrato)
- **Validação automática** de coerência e conformidade legal
- **Exportação institucional** em formato `.docx` e `.pdf`
- **Painel Executivo** com indicadores de governança, alertas e insights históricos

---
### ⚙️ Padrões Técnicos
- Linguagem **Python + Streamlit**
- Estrutura modular baseada em `utils/` e `validators/`
- Trilhas de auditoria armazenadas em `/exports/auditorias/`
- Relatórios automáticos em `/exports/relatorios/`

---
### 📅 Versão e Responsabilidade
- **Versão institucional:** vNext  
- **Responsável técnico:** SAAB / Diretoria de Governança e Inovação  
- **Última atualização:** {}
""".format(datetime.now().strftime("%d/%m/%Y %H:%M")))

# ==========================================================
# 🧭 Rodapé institucional
# ==========================================================
st.markdown("""
<div class="footer">
TJSP • Secretaria de Administração e Abastecimento • SynapseNext – SAAB 5.0<br>
Versão institucional vNext • Desenvolvido em ambiente Python
</div>
""", unsafe_allow_html=True)
