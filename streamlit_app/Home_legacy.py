# ==========================================================
# 🏛️ SynapseNext – SAAB 5.0
# Secretaria de Administração e Abastecimento – TJSP
# Página Inicial (Home)
# ==========================================================

import streamlit as st
from pathlib import Path
import sys

# ==========================================================
# 🔧 Correção de caminho para permitir importações globais
# ==========================================================
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# ==========================================================
# 📦 Importa estilos institucionais
# ==========================================================
from utils.ui_components import aplicar_estilo_global
from utils.ui_style import rodape_institucional

# ==========================================================
# ⚙️ Configurações da Página
# ==========================================================
st.set_page_config(
    page_title="SynapseNext – SAAB 5.0",
    layout="wide",
    page_icon="🏛️"
)

# ==========================================================
# 🎨 Aplicar estilo global padronizado
# ==========================================================
aplicar_estilo_global()

# ==========================================================
# 🏛️ Logo institucional fixo no topo do menu lateral (ajuste final)
# ==========================================================
import base64

logo_path = Path(__file__).resolve().parents[1] / "assets" / "tjsp_logo.png"

if logo_path.exists():
    with open(logo_path, "rb") as f:
        logo_bytes = f.read()
    logo_b64 = base64.b64encode(logo_bytes).decode()

    st.markdown(
        f"""
        <style>
        /* ===== SIDEBAR PROFISSIONAL ===== */
        [data-testid="stSidebar"] {{
            position: relative;
            background: linear-gradient(180deg, #F8F9FB 0%, #FFFFFF 100%) !important;
        }}
        
        /* Cabeçalho do sidebar com logo */
        .sidebar-header {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            text-align: center;
            padding: 1rem 1rem 0.8rem 1rem;
            background: linear-gradient(180deg, #FFFFFF 0%, #F8F9FB 100%);
            z-index: 100;
            border-bottom: 2px solid #E0E4E8;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        }}
        
        .sidebar-header img {{
            max-height: 75px;
            width: auto;
            margin-bottom: 0.6rem;
            filter: drop-shadow(0 1px 3px rgba(0,0,0,0.1));
        }}
        
        /* Espaçamento entre logo e navegação */
        [data-testid="stSidebarNav"] {{
            margin-top: 100px !important;
            padding: 0 0.5rem;
        }}
        
        /* Estilo dos itens de menu */
        [data-testid="stSidebarNav"] ul {{
            padding: 0 !important;
        }}
        
        [data-testid="stSidebarNav"] li {{
            margin-bottom: 0.3rem;
        }}
        
        [data-testid="stSidebarNav"] a {{
            display: flex;
            align-items: center;
            padding: 0.75rem 1rem !important;
            border-radius: 8px;
            font-size: 0.95rem !important;
            font-weight: 500 !important;
            color: #2C3E50 !important;
            background-color: transparent !important;
            transition: all 0.2s ease;
            text-decoration: none !important;
            border: 1px solid transparent;
        }}
        
        /* Hover state - mais sutil e profissional */
        [data-testid="stSidebarNav"] a:hover {{
            background-color: #F0F3F7 !important;
            border-color: #D0D7E0 !important;
            transform: translateX(3px);
            color: #003366 !important;
        }}
        
        /* Item ativo/selecionado */
        [data-testid="stSidebarNav"] a[aria-current="page"] {{
            background: linear-gradient(135deg, #003366 0%, #004488 100%) !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            border-color: #003366 !important;
            box-shadow: 0 2px 6px rgba(0, 51, 102, 0.25);
        }}
        
        /* Ícones dos itens de menu */
        [data-testid="stSidebarNav"] a span {{
            font-size: 1.1rem;
            margin-right: 0.5rem;
        }}
        
        /* Conteúdo adicional do sidebar */
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
            padding: 0.75rem 1rem;
            font-size: 0.9rem;
            color: #4A5568;
        }}
        
        /* Rodapé do sidebar (se houver) */
        [data-testid="stSidebar"] .sidebar-footer {{
            position: absolute;
            bottom: 1rem;
            left: 1rem;
            right: 1rem;
            text-align: center;
            font-size: 0.8rem;
            color: #6B7280;
            padding-top: 1rem;
            border-top: 1px solid #E0E4E8;
        }}
        </style>

        <div class="sidebar-header">
            <img src="data:image/png;base64,{logo_b64}" alt="TJSP Logo">
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==========================================================
# 🏛️ Cabeçalho (sem logo no corpo)
# ==========================================================
st.markdown("""
<div class="titulo-principal">SynapseNext – SAAB 5.0</div>
<div class="subtitulo">Ambiente Institucional de Automação da Fase Interna de Licitação</div>
""", unsafe_allow_html=True)

# ==========================================================
# 🧭 Apresentação institucional
# ==========================================================
st.markdown("""
O **SynapseNext** é um ecossistema digital desenvolvido pela **Secretaria de Administração e Abastecimento (SAAB)** do Tribunal de Justiça de São Paulo, 
destinado a padronizar, auditar e integrar os artefatos que compõem a **fase interna da licitação**, 
de forma automatizada, transparente e aderente à **Lei nº 14.133/2021** e à **Instrução Normativa nº 12/2025**.

Ele conecta módulos inteligentes e pipelines de governança que abrangem todo o ciclo de elaboração:  
**DFD → ETP → TR → Edital → Contrato**, promovendo segurança jurídica, rastreabilidade e eficiência administrativa.
""")

st.markdown("<hr>", unsafe_allow_html=True)

# ==========================================================
# 🧩 Funcionalidades Principais
# ==========================================================
st.markdown("""
### 🌿 Funcionalidades Principais

- **Criação orientada** de artefatos da fase interna (DFD, ETP, TR, Edital e Contrato);
- **Validação automática** de coerência e conformidade legal com base nos checklists institucionais;
- **Exportação institucional** em formato `.docx` e `.pdf` com padronização SAAB/TJSP;
- **Painel Executivo** com indicadores de governança, alertas e insights históricos;
- **Integração nativa** com SharePoint e OneDrive para armazenamento e versionamento controlado.
""")

st.markdown("<hr>", unsafe_allow_html=True)

# ==========================================================
# 🧱 Estrutura Modular
# ==========================================================
st.markdown("""
### 🧱 Estrutura Modular

Cada módulo do SynapseNext está vinculado a um pipeline de auditoria que valida e armazena
os artefatos produzidos, seguindo os parâmetros técnicos da Secretaria de Administração e Abastecimento.

O sistema permite revisão, versionamento e exportação automatizada dos documentos,
mantendo a rastreabilidade entre todas as fases da fase interna da licitação.
""")

# ==========================================================
# 📘 Rodapé institucional
# ==========================================================
rodape_institucional()
