# -*- coding: utf-8 -*-
"""
home_utils/sidebar_organizer.py
Organizador visual da sidebar com agrupamentos semânticos.

Implementa CSS Injection para adicionar títulos de grupos na navegação lateral,
mantendo toda a funcionalidade nativa do Streamlit intacta.
"""

import streamlit as st


def apply_sidebar_grouping():
    """
    Aplica agrupamento visual na sidebar usando CSS customizado.
    
    Grupos implementados:
    - PRODUÇÃO (posições 1-5): Insumos, DFD, ETP, TR, Edital
    - VALIDAÇÃO E CONTROLE (posições 6-8): Validador, Contrato, Alertas
    - GESTÃO (posições 9-11): Análise Desempenho, Painel Governança, Painel Executivo
    - SISTEMA (posições 12-15): Relatório, Comparador, Versão, Integração
    - DOCUMENTAÇÃO (posição 16): Separada com divider
    
    Técnica: CSS ::before pseudo-elements + nth-child selectors
    Compatibilidade: Streamlit 1.28+
    Estética: Institucional TJSP (azul #003366, discreta, minimalista)
    """
    
    css = """
    <style>
    /* ==========================================================
       SIDEBAR - AGRUPAMENTO SEMÂNTICO VISUAL
       ========================================================== */
    
    /* Container da navegação lateral */
    [data-testid="stSidebarNav"] {
        padding-top: 1rem;
    }
    
    /* Espaçamento entre itens */
    [data-testid="stSidebarNav"] ul li {
        margin-bottom: 0.2rem;
    }
    
    /* ==========================================================
       TÍTULOS DE GRUPO (pseudo-elements ::before)
       ========================================================== */
    
    /* 🔹 GRUPO 1: PRODUÇÃO (antes do item 1 - Insumos) */
    [data-testid="stSidebarNav"] ul li:nth-child(1)::before {
        content: "PRODUÇÃO";
        display: block;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        color: #003366;
        text-transform: uppercase;
        margin-top: 0.5rem;
        margin-bottom: 0.6rem;
        margin-left: 0.5rem;
        padding-bottom: 0.3rem;
        border-bottom: 2px solid #003366;
        opacity: 0.85;
    }
    
    /* 🔹 GRUPO 2: VALIDAÇÃO E CONTROLE (antes do item 6 - Validador) */
    [data-testid="stSidebarNav"] ul li:nth-child(6)::before {
        content: "VALIDAÇÃO E CONTROLE";
        display: block;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        color: #003366;
        text-transform: uppercase;
        margin-top: 1.2rem;
        margin-bottom: 0.6rem;
        margin-left: 0.5rem;
        padding-bottom: 0.3rem;
        border-bottom: 2px solid #003366;
        opacity: 0.85;
    }
    
    /* 🔹 GRUPO 3: GESTÃO (antes do item 9 - Análise de Desempenho) */
    [data-testid="stSidebarNav"] ul li:nth-child(9)::before {
        content: "GESTÃO";
        display: block;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        color: #003366;
        text-transform: uppercase;
        margin-top: 1.2rem;
        margin-bottom: 0.6rem;
        margin-left: 0.5rem;
        padding-bottom: 0.3rem;
        border-bottom: 2px solid #003366;
        opacity: 0.85;
    }
    
    /* 🔹 GRUPO 4: SISTEMA (antes do item 12 - Relatório Técnico) */
    [data-testid="stSidebarNav"] ul li:nth-child(12)::before {
        content: "SISTEMA";
        display: block;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        color: #003366;
        text-transform: uppercase;
        margin-top: 1.2rem;
        margin-bottom: 0.6rem;
        margin-left: 0.5rem;
        padding-bottom: 0.3rem;
        border-bottom: 2px solid #003366;
        opacity: 0.85;
    }
    
    /* ==========================================================
       SEPARADOR FINAL (antes da Documentação - item 99)
       ========================================================== */
    
    [data-testid="stSidebarNav"] ul li:last-child::before {
        content: "";
        display: block;
        height: 1px;
        background: linear-gradient(to right, transparent, #003366 20%, #003366 80%, transparent);
        margin: 1.5rem 0.5rem 0.8rem 0.5rem;
        opacity: 0.4;
    }
    
    /* ==========================================================
       REFINAMENTOS VISUAIS
       ========================================================== */
    
    /* Links - manter destaque do item ativo */
    [data-testid="stSidebarNav"] a {
        transition: background-color 0.2s ease;
    }
    
    /* Hover suave nos links */
    [data-testid="stSidebarNav"] a:hover {
        background-color: rgba(0, 51, 102, 0.08) !important;
    }
    
    /* Item ativo - reforçar destaque */
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background-color: rgba(0, 51, 102, 0.12) !important;
        border-left: 3px solid #003366;
        font-weight: 600;
    }
    
    /* ==========================================================
       RESPONSIVIDADE (sidebar colapsada)
       ========================================================== */
    
    @media (max-width: 768px) {
        /* Títulos de grupo menores em mobile */
        [data-testid="stSidebarNav"] ul li::before {
            font-size: 0.65rem !important;
            margin-left: 0.3rem !important;
        }
    }
    
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)


def render_sidebar_info():
    """
    Adiciona informação contextual no rodapé da sidebar (opcional).
    Pode ser chamado em páginas específicas se necessário.
    """
    with st.sidebar:
        st.markdown("---")
        st.caption("🏛️ **TJSP** | Projeto SAAB-Tech")
        st.caption("v2025.1 • Homologação")
