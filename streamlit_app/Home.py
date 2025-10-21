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
# 🏛️ Logo institucional fixo no menu lateral
# ==========================================================
logo_path = Path(__file__).resolve().parents[1] / "assets" / "tjsp_logo.png"
if logo_path.exists():
    st.sidebar.image(str(logo_path), use_column_width=True)
st.sidebar.markdown("---")

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
