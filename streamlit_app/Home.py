# ==============================================================
# SynapseNext – Fase Brasília
# Página Inicial (Home)
# ==============================================================
# Versão 2025-10-20 | Autor: Carlos Darwin de Mattos
# ==============================================================
import streamlit as st
from pathlib import Path

# --------------------------------------------------------------
# Configuração da página
# --------------------------------------------------------------
st.set_page_config(
    page_title="SynapseNext – Home",
    layout="wide",
    page_icon="🧭"
)

# --------------------------------------------------------------
# Caminho e verificação do logotipo TJSP
# --------------------------------------------------------------
LOGO_PATH = Path(__file__).resolve().parents[1] / "utils" / "assets" / "tjsp_logo.png"

# --------------------------------------------------------------
# Estilos customizados (baseado no manual de identidade TJSP)
# --------------------------------------------------------------
st.markdown("""
<style>
/* ===== HEADER ===== */
.header-wrap {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    margin: 20px 0 12px 0;
}
.header-logo img {
    width: 180px;
    height: auto;
    object-fit: contain;
}
.header-title h1 {
    margin: 0;
    font-size: 2.2rem;
    color: #000000;
    line-height: 1.2;
}
.header-title p {
    margin: 4px 0 0 0;
    font-size: 1.05rem;
    color: #666666;
}
.divider {
    height: 1px;
    background-color: #e8e8e8;
    margin: 12px 0 24px 0;
}

/* ===== CARDS DE ATALHO ===== */
.cards-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 20px;
    margin-top: 24px;
}
.card {
    background-color: #ffffff;
    border: 1px solid #dddddd;
    border-radius: 14px;
    padding: 22px 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    transition: all 0.2s ease-in-out;
}
.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    border-color: #990000; /* vermelho TJSP */
}
.card h4 {
    margin: 0 0 6px 0;
    color: #990000;
}
.card p {
    color: #555555;
    font-size: 0.95rem;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------
# Header institucional
# --------------------------------------------------------------
st.markdown('<div class="header-wrap">', unsafe_allow_html=True)
if LOGO_PATH.exists():
    st.markdown('<div class="header-logo">', unsafe_allow_html=True)
    st.image(str(LOGO_PATH), use_column_width=False)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="header-logo"></div>', unsafe_allow_html=True)

st.markdown('<div class="header-title">', unsafe_allow_html=True)
st.markdown("<h1>SynapseNext – Hub Institucional</h1>", unsafe_allow_html=True)
st.markdown("<p>Secretaria de Administração e Abastecimento • Fase Brasília</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div><div class="divider"></div>', unsafe_allow_html=True)

# --------------------------------------------------------------
# Seção descritiva – Objetivo da página
# --------------------------------------------------------------
st.markdown("""
### 🧭 O que você encontra aqui
Esta é a **página inicial** do ecossistema **SynapseNext**, plataforma integrada para apoio à **Fase Interna da Licitação** do Tribunal de Justiça de São Paulo.

Use o **menu lateral** para navegar entre os módulos:
- **Documentos e Governança:** acompanhe indicadores e relatórios técnicos.  
- **Alertas e Auditoria:** visualize inconsistências detectadas e status de coerência.  
- **Insights Históricos:** explore a evolução dos dados e tendências de governança.  
- **Painel Executivo:** acesse o resumo consolidado, com gráficos e relatórios PDF.

Todas as etapas seguem os padrões institucionais do **TJSP / SAAB**, respeitando a **Instrução Normativa nº 12/2025**.
""")

# --------------------------------------------------------------
# Cartões de Atalho (atalhos rápidos)
# --------------------------------------------------------------
st.markdown('<div class="cards-container">', unsafe_allow_html=True)

st.markdown("""
<div class="card">
    <h4>📑 Relatórios Técnicos</h4>
    <p>Gere e valide artefatos como DFD, ETP e TR, com auditoria integrada e exportação automatizada.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">
    <h4>⚙️ Painel de Governança</h4>
    <p>Monitore indicadores de coerência, auditoria e trilhas de controle em tempo real.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">
    <h4>⚠️ Alertas Proativos</h4>
    <p>Acompanhe notificações sobre inconsistências, staleness e variações textuais.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">
    <h4>💡 Insights Históricos</h4>
    <p>Analise a evolução da coerência global, volume de auditorias e médias móveis de desempenho.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">
    <h4>📊 Painel Executivo</h4>
    <p>Visualize KPIs, gráficos e relatórios executivos integrados ao ambiente institucional do TJSP.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------------------
# Rodapé institucional
# --------------------------------------------------------------
st.markdown("""
<div style='text-align:center; margin-top:40px; color:#666666; font-size:0.9rem;'>
TJSP • Secretaria de Administração e Abastecimento (SAAB) • Projeto SynapseNext – Fase Brasília<br>
Versão institucional vNext • Desenvolvido em ambiente Python + Streamlit
</div>
""", unsafe_allow_html=True)
