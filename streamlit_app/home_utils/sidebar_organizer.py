# -*- coding: utf-8 -*-
"""
home_utils/sidebar_organizer.py
Organizador visual da sidebar com agrupamentos por bordas coloridas.

Implementa CSS Injection para criar efeito de "botões agrupados" na navegação,
usando bordas laterais discretas em cores institucionais para sugerir contexto,
sem títulos ou textos fixos.
"""

import streamlit as st


def apply_sidebar_grouping():
    """
    Aplica agrupamento visual sutil na sidebar usando bordas coloridas.
    
    Grupos visuais (por cor de borda):
    - PRODUÇÃO (1-4): azul escuro - Insumos, DFD, ETP, TR
    - VALIDAÇÃO/CONTRATAÇÃO (5-7): verde institucional - Edital, Validador, Contrato
    - MONITORAMENTO (8-9): laranja suave - Alertas, Análise Desempenho
    - GOVERNANÇA (10-12): roxo institucional - Painéis e Relatório
    - UTILITÁRIOS (13-15): cinza - Comparador, Versão, Integração
    - DOCUMENTAÇÃO (16): sem borda especial
    
    Técnica: bordas left de 3px + background sutil + border-radius
    Visual: efeito de "botões" discretos, sem textos de agrupamento
    """
    
    css = """
    <style>
    /* ==========================================================
       SIDEBAR - AGRUPAMENTO VISUAL POR BORDAS COLORIDAS
       ========================================================== */
    
    /* Base: todos os itens como "botões" com cantos arredondados */
    [data-testid="stSidebarNav"] ul li a {
        border-radius: 6px !important;
        margin: 0.15rem 0.5rem !important;
        padding: 0.5rem 0.75rem !important;
        transition: all 0.2s ease !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
        border-left: 3px solid transparent !important;
    }
    
    /* Hover suave para todos os itens */
    [data-testid="stSidebarNav"] ul li a:hover {
        background-color: rgba(0, 0, 0, 0.03) !important;
        transform: translateX(2px);
    }
    
    /* ==========================================================
       GRUPO 1: PRODUÇÃO (azul institucional TJSP)
       Itens 1-4: Insumos, DFD, ETP, TR
       ========================================================== */
    
    [data-testid="stSidebarNav"] ul li:nth-child(1) a,
    [data-testid="stSidebarNav"] ul li:nth-child(2) a,
    [data-testid="stSidebarNav"] ul li:nth-child(3) a,
    [data-testid="stSidebarNav"] ul li:nth-child(4) a {
        border-left-color: #003366 !important;
        background-color: rgba(0, 51, 102, 0.02) !important;
    }
    
    [data-testid="stSidebarNav"] ul li:nth-child(1) a:hover,
    [data-testid="stSidebarNav"] ul li:nth-child(2) a:hover,
    [data-testid="stSidebarNav"] ul li:nth-child(3) a:hover,
    [data-testid="stSidebarNav"] ul li:nth-child(4) a:hover {
        background-color: rgba(0, 51, 102, 0.06) !important;
    }
    
    /* ==========================================================
       GRUPO 2: VALIDAÇÃO/CONTRATAÇÃO (verde institucional)
       Itens 5-7: Edital, Validador, Contrato
       ========================================================== */
    
    [data-testid="stSidebarNav"] ul li:nth-child(5) a,
    [data-testid="stSidebarNav"] ul li:nth-child(6) a,
    [data-testid="stSidebarNav"] ul li:nth-child(7) a {
        border-left-color: #2d5c3f !important;
        background-color: rgba(45, 92, 63, 0.02) !important;
    }
    
    [data-testid="stSidebarNav"] ul li:nth-child(5) a:hover,
    [data-testid="stSidebarNav"] ul li:nth-child(6) a:hover,
    [data-testid="stSidebarNav"] ul li:nth-child(7) a:hover {
        background-color: rgba(45, 92, 63, 0.06) !important;
    }
    
    /* ==========================================================
       GRUPO 3: MONITORAMENTO (laranja suave)
       Itens 8-9: Alertas, Análise Desempenho
       ========================================================== */
    
    [data-testid="stSidebarNav"] ul li:nth-child(8) a,
    [data-testid="stSidebarNav"] ul li:nth-child(9) a {
        border-left-color: #c8741a !important;
        background-color: rgba(200, 116, 26, 0.02) !important;
    }
    
    [data-testid="stSidebarNav"] ul li:nth-child(8) a:hover,
    [data-testid="stSidebarNav"] ul li:nth-child(9) a:hover {
        background-color: rgba(200, 116, 26, 0.06) !important;
    }
    
    /* ==========================================================
       GRUPO 4: GOVERNANÇA (roxo institucional)
       Itens 10-12: Painel Governança, Painel Executivo, Relatório
       ========================================================== */
    
    [data-testid="stSidebarNav"] ul li:nth-child(10) a,
    [data-testid="stSidebarNav"] ul li:nth-child(11) a,
    [data-testid="stSidebarNav"] ul li:nth-child(12) a {
        border-left-color: #5b3a7d !important;
        background-color: rgba(91, 58, 125, 0.02) !important;
    }
    
    [data-testid="stSidebarNav"] ul li:nth-child(10) a:hover,
    [data-testid="stSidebarNav"] ul li:nth-child(11) a:hover,
    [data-testid="stSidebarNav"] ul li:nth-child(12) a:hover {
        background-color: rgba(91, 58, 125, 0.06) !important;
    }
    
    /* ==========================================================
       GRUPO 5: UTILITÁRIOS (cinza neutro)
       Itens 13-15: Comparador, Versão, Integração
       ========================================================== */
    
    [data-testid="stSidebarNav"] ul li:nth-child(13) a,
    [data-testid="stSidebarNav"] ul li:nth-child(14) a,
    [data-testid="stSidebarNav"] ul li:nth-child(15) a {
        border-left-color: #6c757d !important;
        background-color: rgba(108, 117, 125, 0.02) !important;
    }
    
    [data-testid="stSidebarNav"] ul li:nth-child(13) a:hover,
    [data-testid="stSidebarNav"] ul li:nth-child(14) a:hover,
    [data-testid="stSidebarNav"] ul li:nth-child(15) a:hover {
        background-color: rgba(108, 117, 125, 0.06) !important;
    }
    
    /* ==========================================================
       DOCUMENTAÇÃO (16): destaque especial com divider visual
       ========================================================== */
    
    /* Separador visual antes da documentação */
    [data-testid="stSidebarNav"] ul li:nth-child(16) {
        margin-top: 1rem !important;
        padding-top: 1rem !important;
        border-top: 1px solid rgba(0, 0, 0, 0.1);
    }
    
    [data-testid="stSidebarNav"] ul li:nth-child(16) a {
        border-left-color: #003366 !important;
        background-color: rgba(0, 51, 102, 0.03) !important;
        font-weight: 500 !important;
    }
    
    /* ==========================================================
       ITEM ATIVO (aria-current="page")
       Reforça destaque com borda mais grossa e background
       ========================================================== */
    
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        border-left-width: 4px !important;
        font-weight: 600 !important;
        background-color: rgba(0, 0, 0, 0.08) !important;
    }
    
    /* Itens ativos por grupo mantêm cor da borda */
    [data-testid="stSidebarNav"] ul li:nth-child(1) a[aria-current="page"],
    [data-testid="stSidebarNav"] ul li:nth-child(2) a[aria-current="page"],
    [data-testid="stSidebarNav"] ul li:nth-child(3) a[aria-current="page"],
    [data-testid="stSidebarNav"] ul li:nth-child(4) a[aria-current="page"] {
        background-color: rgba(0, 51, 102, 0.12) !important;
    }
    
    [data-testid="stSidebarNav"] ul li:nth-child(5) a[aria-current="page"],
    [data-testid="stSidebarNav"] ul li:nth-child(6) a[aria-current="page"],
    [data-testid="stSidebarNav"] ul li:nth-child(7) a[aria-current="page"] {
        background-color: rgba(45, 92, 63, 0.12) !important;
    }
    
    [data-testid="stSidebarNav"] ul li:nth-child(8) a[aria-current="page"],
    [data-testid="stSidebarNav"] ul li:nth-child(9) a[aria-current="page"] {
        background-color: rgba(200, 116, 26, 0.12) !important;
    }
    
    [data-testid="stSidebarNav"] ul li:nth-child(10) a[aria-current="page"],
    [data-testid="stSidebarNav"] ul li:nth-child(11) a[aria-current="page"],
    [data-testid="stSidebarNav"] ul li:nth-child(12) a[aria-current="page"] {
        background-color: rgba(91, 58, 125, 0.12) !important;
    }
    
    [data-testid="stSidebarNav"] ul li:nth-child(13) a[aria-current="page"],
    [data-testid="stSidebarNav"] ul li:nth-child(14) a[aria-current="page"],
    [data-testid="stSidebarNav"] ul li:nth-child(15) a[aria-current="page"] {
        background-color: rgba(108, 117, 125, 0.12) !important;
    }
    
    /* ==========================================================
       ESPAÇAMENTO ENTRE GRUPOS
       Adiciona margem superior ao primeiro item de cada grupo
       ========================================================== */
    
    [data-testid="stSidebarNav"] ul li:nth-child(5),
    [data-testid="stSidebarNav"] ul li:nth-child(8),
    [data-testid="stSidebarNav"] ul li:nth-child(10),
    [data-testid="stSidebarNav"] ul li:nth-child(13) {
        margin-top: 0.8rem !important;
    }
    
    /* ==========================================================
       RESPONSIVIDADE
       ========================================================== */
    
    @media (max-width: 768px) {
        [data-testid="stSidebarNav"] ul li a {
            margin: 0.1rem 0.3rem !important;
            padding: 0.4rem 0.6rem !important;
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
