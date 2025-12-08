# Atualização forçada para recarregar módulos - vNext
# -*- coding: utf-8 -*-
# ==============================================================
# Projeto SAAB-Tech
# Página Inicial (Home v5 – Interoperabilidade Institucional)
# ==============================================================
# Versão institucional vNext+ – Novembro/2025
# ==============================================================

# --------------------------------------------------------------
# 🔧 Correção de contexto de execução para Streamlit Cloud
# --------------------------------------------------------------
import sys
from pathlib import Path

# Garante que a pasta raiz do projeto seja reconhecida pelo Python
base_path = Path(__file__).resolve().parents[1]
if str(base_path) not in sys.path:
    sys.path.insert(0, str(base_path))

# --------------------------------------------------------------
# Imports principais
# --------------------------------------------------------------
import streamlit as st
import base64
from datetime import datetime

# --------------------------------------------------------------
# Configuração da página
# --------------------------------------------------------------
st.set_page_config(
    page_title="Projeto SAAB-Tech | Interoperabilidade Institucional",
    layout="wide",
    page_icon="🧭"
)

# --------------------------------------------------------------
# Caminho da imagem institucional (bandeira TJSP)
# --------------------------------------------------------------
LOGO_PATH = base_path / "assets" / "tjsp_logo.png"

def get_base64_image(path: Path) -> str:
    """Retorna imagem em base64 para exibição inline"""
    if path.exists():
        return base64.b64encode(path.read_bytes()).decode()
    return ""

LOGO_BASE64 = get_base64_image(LOGO_PATH)

# --------------------------------------------------------------
# Estilos customizados (SAAB 5.0)
# --------------------------------------------------------------
st.markdown("""
<style>
section.main > div { padding-top: 10px !important; }
.block-container { padding-top: 0rem !important; }

/* ======= CABEÇALHO ======= */
.header-wrap {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    margin: -10px 0 10px 0;
}
.header-logo img { width: 165px; object-fit: contain; }
.header-title h1 {
    margin: 0;
    font-size: 2.4rem;
    color: #990000;
    line-height: 1.2;
    font-weight: 700;
}
.header-title p {
    margin: 3px 0 0 0;
    font-size: 1rem;
    color: #444444;
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
    transform: translateY(-3px);
    box-shadow: 0 4px 10px rgba(153,0,0,0.25);
    border-color: #990000;
}
.card h4 {
    margin: 0 0 6px 0;
    color: #990000;
    font-weight: 600;
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
.footer img { width: 70px; opacity: 0.35; margin-top: 5px; }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------
# Cabeçalho com logotipo e título institucional
# --------------------------------------------------------------
st.markdown('<div class="header-wrap">', unsafe_allow_html=True)

st.markdown("""
<div class="header-title">
    <h1>Projeto SAAB-Tech</h1>
    <p>Secretaria de Administração e Abastecimento • Tribunal de Justiça de São Paulo</p>
</div>
""", unsafe_allow_html=True)
st.markdown('</div><div class="divider"></div>', unsafe_allow_html=True)

# --------------------------------------------------------------
# Conteúdo introdutório
# --------------------------------------------------------------
st.markdown("""
### 🧭 Bem-vindo ao SynapseNext
O **Projeto SAAB-Tech** é o ecossistema institucional de automação inteligente que apoia a **Fase Interna da Licitação**, conforme a **Lei nº 14.133/2021** e a **Instrução Normativa nº 12/2025**.

Aqui você encontra todos os módulos que compõem a jornada digital do processo de contratação pública:
- **Insumos, DFD, ETP, TR e Edital:** geração assistida por IA, análise normativa e validação técnica.  
- **Relatórios e Governança:** acompanhamento de coerência, integridade e conformidade.  
- **Painéis Executivo e de Qualidade:** indicadores de performance institucional.  
- **🧩 Interoperabilidade:** integração com sistemas externos e plataformas de gestão documental.
""")

# --------------------------------------------------------------
# Cartões de navegação rápida
# --------------------------------------------------------------
st.markdown('<div class="cards-container">', unsafe_allow_html=True)

cards = [
    ("📘 Documentos Técnicos", "Produza e valide os artefatos institucionais da Fase Interna: DFD, ETP, TR e Edital."),
    ("📊 Painel Executivo", "Visualize indicadores, KPIs e métricas de desempenho em tempo real."),
    ("⚙️ Painel de Governança", "Monitore a coerência global dos artefatos e a rastreabilidade das decisões."),
    ("🧩 Interoperabilidade", "Gerencie conexões seguras com SharePoint, OneDrive, GitHub e OpenAI."),
    ("📑 Relatórios Técnicos", "Gere auditorias e relatórios integrados em formatos DOCX e PDF."),
]

for title, desc in cards:
    st.markdown(f"<div class='card'><h4>{title}</h4><p>{desc}</p></div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------------------
# Seção futura: Manual e Recursos
# --------------------------------------------------------------
st.markdown("""
---
### 📘 Manual e Recursos (em breve)
Esta área exibirá o **Manual do Usuário SAAB 5.0** e tutoriais interativos sobre o uso de cada módulo,
incluindo vídeos e orientações sobre as boas práticas de interoperabilidade institucional.
""")

# --------------------------------------------------------------
# Rodapé institucional
# --------------------------------------------------------------
st.markdown(f"""
<div class="footer">
TJSP • Secretaria de Administração e Abastecimento • Projeto SAAB-Tech<br>
• Build gerado em {datetime.now():%d/%m/%Y %H:%M}
</div>
""", unsafe_allow_html=True)

if LOGO_BASE64:
    st.markdown(f"<div style='text-align:center;'><img src='data:image/png;base64,{LOGO_BASE64}' alt='TJSP'></div>", unsafe_allow_html=True)
