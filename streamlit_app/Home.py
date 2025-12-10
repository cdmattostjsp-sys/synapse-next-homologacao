# Atualização forçada para recarregar módulos - vNext
# -*- coding: utf-8 -*-
# ==============================================================
# Projeto SAAB-Tech
# Página Inicial (Home v6 – Arquitetura Modular + Documentação)
# ==============================================================
# Versão institucional vNext+ – Dezembro/2025
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

# Adiciona o diretório streamlit_app ao path para imports locais
streamlit_app_path = Path(__file__).resolve().parent
if str(streamlit_app_path) not in sys.path:
    sys.path.insert(0, str(streamlit_app_path))

# --------------------------------------------------------------
# Imports principais
# --------------------------------------------------------------
import streamlit as st
import base64

# --------------------------------------------------------------
# Imports modulares (NOVO - Arquitetura modular)
# --------------------------------------------------------------
from utils.home_components import (
    render_custom_css,
    render_header,
    render_intro,
    render_cards,
    render_manuais_section,
    render_footer
)

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

# ==============================================================
# ESTRUTURA MODULAR DA PÁGINA (REFATORADO v6)
# ==============================================================

# Renderiza estilos CSS customizados
render_custom_css()

# Renderiza cabeçalho institucional
render_header()

# Renderiza seção de introdução
render_intro()

# Renderiza cards de navegação
render_cards()

# Renderiza seção de manuais (NOVA FUNCIONALIDADE)
render_manuais_section()

# Renderiza rodapé institucional
render_footer(LOGO_BASE64)
