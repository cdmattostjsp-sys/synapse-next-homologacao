# -*- coding: utf-8 -*-
"""
Componentes modulares da página Home do Projeto SAAB-Tech
Separação de responsabilidades para facilitar manutenção e escalabilidade
Versão: 2025.1
"""

import streamlit as st
from datetime import datetime


def render_custom_css():
    """Renderiza estilos CSS customizados do SAAB 5.0"""
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
    
    /* ======= SEÇÃO MANUAIS ======= */
    .manuais-section {
        background-color: #f8f9fa;
        border-radius: 12px;
        padding: 24px;
        margin-top: 32px;
        border: 1px solid #e0e0e0;
    }
    .manual-card {
        background-color: #ffffff;
        border: 1px solid #dddddd;
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 12px;
        transition: all 0.2s ease-in-out;
    }
    .manual-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 3px 8px rgba(153,0,0,0.15);
        border-color: #990000;
    }
    .manual-card h5 {
        margin: 0 0 8px 0;
        color: #990000;
        font-size: 1.1rem;
    }
    .manual-card p {
        margin: 0;
        color: #666666;
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)


def render_header():
    """Renderiza cabeçalho institucional com título e subtítulo"""
    st.markdown('<div class="header-wrap">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="header-title">
        <h1>Projeto SAAB-Tech</h1>
        <p>Secretaria de Administração e Abastecimento • Tribunal de Justiça de São Paulo</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div><div class="divider"></div>', unsafe_allow_html=True)


def render_intro():
    """Renderiza seção de introdução e boas-vindas"""
    st.markdown("""
    ### 🧭 Bem-vindo(a)
    O **Projeto SAAB-Tech** é o ecossistema institucional de automação inteligente que apoia a **Fase Interna da Licitação**, a elaboração de editais, auditorias e contratos, tudo conforme previsto na **Lei nº 14.133/2021** e a **Instrução Normativa nº 12/2025**.

    Aqui você encontra todos os módulos que compõem a jornada digital do processo de contratação pública:
    - **Insumos, DFD, ETP, TR e Edital:** geração assistida por IA, análise normativa e validação técnica.  
    - **Relatórios e Governança:** acompanhamento de coerência, integridade e conformidade.  
    - **Painéis Executivo e de Qualidade:** indicadores de performance institucional.  
    - **Interoperabilidade:** integração com sistemas externos e plataformas de gestão documental.
    """)


def render_cards():
    """Renderiza grid de cards com módulos do sistema"""
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


def render_manuais_section():
    """Renderiza seção de acesso aos manuais do usuário"""
    st.markdown("---")
    st.markdown("### 📚 Documentação do Sistema")
    st.markdown("""
    Acesse os manuais completos do Projeto SAAB-Tech com guias detalhados sobre cada módulo,
    casos práticos e soluções para problemas comuns.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='manual-card'>
            <h5>📖 Manuais Básicos</h5>
            <p>Introdução, Planejamento e Edital</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Acessar Manuais Básicos", use_container_width=True, key="btn_basico"):
            st.switch_page("pages/99_📚_Documentação.py")
    
    with col2:
        st.markdown("""
        <div class='manual-card'>
            <h5>🎓 Módulos Avançados</h5>
            <p>Governança, Relatórios e Integração</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Acessar Módulos Avançados", use_container_width=True, key="btn_avanc"):
            st.switch_page("pages/99_📚_Documentação.py")
    
    with col3:
        st.markdown("""
        <div class='manual-card'>
            <h5>🆘 Suporte</h5>
            <p>FAQ e Troubleshooting</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Acessar FAQ e Ajuda", use_container_width=True, key="btn_faq"):
            st.switch_page("pages/99_📚_Documentação.py")


def render_footer(logo_base64: str = ""):
    """Renderiza rodapé institucional com informações e logo"""
    st.markdown(f"""
    <div class="footer">
    TJSP • Secretaria de Administração e Abastecimento • Projeto SAAB-Tech<br>
    • Build gerado em {datetime.now():%d/%m/%Y %H:%M}
    </div>
    """, unsafe_allow_html=True)
    
    if logo_base64:
        st.markdown(
            f"<div style='text-align:center;'><img src='data:image/png;base64,{logo_base64}' alt='TJSP'></div>", 
            unsafe_allow_html=True
        )
