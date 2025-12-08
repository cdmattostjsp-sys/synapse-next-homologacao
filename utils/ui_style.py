# ==========================================================
# 🎨 SynapseNext – Estilo Institucional Global
# Secretaria de Administração e Abastecimento (SAAB 5.0)
# ==========================================================
# Este módulo define o padrão visual aplicado a todas as
# páginas do ecossistema SynapseNext.
# Basta importar e chamar aplicar_estilo_institucional()
# no início de cada página Streamlit.
# ==========================================================

import streamlit as st
from datetime import datetime

# ==========================================================
# 🎨 Função principal – Aplicar estilo institucional
# ==========================================================
def aplicar_estilo_institucional():
    """
    Injeta o CSS institucional padrão do TJSP / SAAB
    em todas as páginas do SynapseNext.
    """
    st.markdown("""
    <style>
    /* =======================================================
       FONTES E HIERARQUIA TIPOGRÁFICA
    ======================================================= */
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
        color: #333333;
    }

    h1, h2, h3, h4, h5 {
        font-family: 'Segoe UI', sans-serif;
        color: #333333;
        margin-bottom: 0.4rem;
    }

    h1 {
        font-size: 1.6rem !important;
        font-weight: 600;
        color: #444;
    }

    h2 {
        font-size: 1.2rem !important;
        font-weight: 500;
        color: #555;
    }

    h3 {
        font-size: 1.05rem !important;
        font-weight: 500;
        color: #666;
    }

    p, li {
        font-size: 0.95rem !important;
        color: #444;
        line-height: 1.5rem;
    }

    /* =======================================================
       ELEMENTOS VISUAIS E ESPAÇAMENTO
    ======================================================= */
    hr {
        border: 0;
        height: 1px;
        background: #dddddd;
        margin: 1.5rem 0;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    .stButton > button {
        background-color: #b71c1c !important;  /* Vermelho TJSP */
        color: white !important;
        border-radius: 6px !important;
        border: none !important;
        padding: 0.5rem 1.2rem;
        font-size: 0.9rem !important;
        font-weight: 500;
        transition: background-color 0.2s ease-in-out;
    }

    .stButton > button:hover {
        background-color: #8b0000 !important;
        color: #fff !important;
    }

    /* =======================================================
       ALERTAS, PROGRESSOS E INFOS
    ======================================================= */
    .stAlert > div {
        font-size: 0.9rem !important;
    }

    .stProgress > div > div > div > div {
        background-color: #b71c1c !important;  /* Vermelho institucional */
    }

    /* =======================================================
       RODAPÉ INSTITUCIONAL
    ======================================================= */
    .footer {
        text-align: center;
        color: gray;
        font-size: 0.85rem;
        margin-top: 3rem;
        padding-top: 0.5rem;
        border-top: 1px solid #dddddd;
    }

    /* =======================================================
       CABEÇALHO E LOGO
    ======================================================= */
    .logo-container {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .logo-container img {
        height: 42px;
        margin-top: -4px;
    }

    /* =======================================================
       TABELAS E TEXTOS DETALHADOS
    ======================================================= */
    table {
        border-collapse: collapse;
        width: 100%;
        margin-top: 1rem;
    }

    th, td {
        border: 1px solid #ddd;
        padding: 0.5rem;
        text-align: left;
        font-size: 0.9rem;
    }

    th {
        background-color: #f6f6f6;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)


# ==========================================================
# 🧾 Função auxiliar – Rodapé institucional
# ==========================================================
def rodape_institucional():
    """
    Exibe o rodapé institucional padrão com
    data e versão dinâmica.
    """
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
    st.markdown(f"""
    <div class="footer">
        TJSP • Secretaria de Administração e Abastecimento • Projeto SAAB-Tech<br>
        Versão institucional vNext • Atualizado em {data_atual}<br>
        Desenvolvido em ambiente Python / Streamlit
    </div>
    """, unsafe_allow_html=True)

# --- Funções de compatibilidade SAAB 5.0 ---

def aplicar_tema():
    """Aplica tema padrão SAAB 5.0 (compatibilidade com versões anteriores)."""
    import streamlit as st

    st.markdown(
        """
        <style>
        :root {
            --cor-primaria: #004A8F;
            --cor-secundaria: #007ACC;
            --cor-sucesso: #00A86B;
            --cor-erro: #D72638;
            --fonte-base: 'Inter', sans-serif;
        }
        body {
            font-family: var(--fonte-base);
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    return "Tema SAAB 5.0 aplicado"

# Atributos auxiliares esperados pelos testes
cor_primaria = "#004A8F"
fonte_base = "Inter"

# ==========================================================
# 🔄 Alias de compatibilidade – manter compatibilidade com o layout SAAB 5.0
# ==========================================================
aplicar_estilo_global = aplicar_estilo_institucional
