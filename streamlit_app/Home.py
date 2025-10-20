# ==============================================================
# SynapseNext – Fase Brasília
# Página Inicial (Home v3)
# ==============================================================
# Versão 2025-10-20 | Autor: Carlos Darwin de Mattos
# ==============================================================
import streamlit as st
from pathlib import Path
import base64

# --------------------------------------------------------------
# Configuração da página
# --------------------------------------------------------------
st.set_page_config(
    page_title="SynapseNext – Hub Institucional",
    layout="wide",
    page_icon="🧭"
)

# --------------------------------------------------------------
# Caminho da imagem institucional
# --------------------------------------------------------------
LOGO_PATH = Path(__file__).resolve().parents[1] / "utils" / "assets" / "tjsp_logo.png"

def get_base64_image(path: Path) -> str:
    """Retorna imagem em base64 para exibição inline"""
    if path.exists():
        return base64.b64encode(path.read_bytes()).decode()
    return ""

LOGO_BASE64 = get_base64_image(LOGO_PATH)

# --------------------------------------------------------------
# Estilos customizados
# --------------------------------------------------------------
st.markdown("""
<style>
/* ======= RESET E BASE ======= */
section.main > div {
    padding-top: 10px !important; /* reduz espaço superior */
}
.block-container {
    padding-top: 0rem !important;
}

/* ======= HEADER ======= */
.header-wrap {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    margin: -10px 0 10px 0;
}
.header-logo img {
    width: 170px;
    height: auto;
    object-fit: contain;
}
.header-title h1 {
    margin: 0;
    font-size: 2.3rem;
    color: #000000;
    line-height: 1.2;
}
.header-title p {
    margin: 3px 0 0 0;
    font-size: 1rem;
    color: #666666;
}
.divider {
    height: 1px;
    background-color: #e8e8e8;
    margin: 12px 0 24px 0;
}

/* ======= CARTÕES ======= */
.cards-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 18px;
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

/* ======= RODAPÉ ======= */
.footer {
    text-align:center;
    margin-top:40px;
    color:#666666;
    font-size:0.9rem;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------
# Cabeçalho com logotipo embutido e título
# --------------------------------------------------------------
st.markdown('<div class="header-wrap">', unsafe_allow_html=True)

# logotipo (lado esquerdo)
if LOGO_BASE64:
    st.markdown(
        f"""
        <div class="header-logo">
            <img src="data:image/png;base64,{LOGO_BASE64}" alt="TJSP">
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown('<div class="header-logo"></div>', unsafe_allow_html=True)

# título e subtítulo
st.markdown('<div class="header-title">', unsafe_allow_html=True)
st.markdown("<h1>SynapseNext – Hub Institucional</h1>", unsafe_allow_html=True)
st.markdown("<p>Secretaria de Administração e Abastecimento • Fase Brasília</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div><div class="divider"></div>', unsafe_allow_html=True)

# --------------------------------------------------------------
# Texto introdutório – finalidade da página
# --------------------------------------------------------------
st.markdown("""
### 🧭 O que você encontra aqui
Esta é a **página inicial** do ecossistema **SynapseNext**, uma plataforma integrada para apoio à **Fase Interna da Licitação** do Tribunal de Justiça de São Paulo.

Use o **menu lateral** para navegar entre os módulos principais:
- **Documentos e Governança:** acompanhe indicadores e relatórios técnicos.  
- **Alertas e Auditoria:** visualize inconsistências detectadas e status de coerência.  
- **Insights Históricos:** explore a evolução dos dados e tendências de governança.  
- **Painel Executivo:** acesse o resumo consolidado, com gráficos e relatórios PDF.

Todas as etapas seguem os padrões institucionais do **TJSP / SAAB**, conforme a **Instrução Normativa nº 12/2025**.
""")

# --------------------------------------------------------------
# Cartões de navegação rápida
# --------------------------------------------------------------
st.markdown('<div class="cards-container">', unsafe_allow_html=True)

cards = [
    ("📑 Relatórios Técnicos", "Gere e valide artefatos como DFD, ETP e TR, com auditoria integrada e exportação automatizada."),
    ("⚙️ Painel de Governança", "Monitore indicadores de coerência, auditoria e trilhas de controle em tempo real."),
    ("⚠️ Alertas Proativos", "Acompanhe notificações sobre inconsistências, staleness e variações textuais."),
    ("💡 Insights Históricos", "Analise a evolução da coerência global, volume de auditorias e médias móveis de desempenho."),
    ("📊 Painel Executivo", "Visualize KPIs, gráficos e relatórios executivos integrados ao ambiente institucional do TJSP.")
]

for title, desc in cards:
    st.markdown(f"""
    <div class="card">
        <h4>{title}</h4>
        <p>{desc}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------------------
# Rodapé institucional com selo do TJSP
# --------------------------------------------------------------
st.markdown("""
<div class="footer">
TJSP • Secretaria de Administração e Abastecimento (SAAB) • Projeto SynapseNext – Fase Brasília<br>
Versão institucional vNext • Desenvolvido em ambiente Python + Streamlit
</div>
""", unsafe_allow_html=True)

if LOGO_BASE64:
    st.markdown(
        f"""
        <div style='text-align:center; margin-top:8px;'>
            <img src="data:image/png;base64,{LOGO_BASE64}" 
                 alt="TJSP" style="width:72px; opacity:0.35;">
        </div>
        """,
        unsafe_allow_html=True
    )
