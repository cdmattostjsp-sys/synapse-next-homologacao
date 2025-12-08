import streamlit as st

# ==========================================================
# 🎨 Estilo global e cabeçalho padrão do Projeto SAAB-Tech
# ==========================================================

def aplicar_estilo_global():
    """
    Aplica o CSS global padronizado a todas as páginas.
    Chame esta função no topo de cada página após st.set_page_config(...).
    """
    st.markdown(
        """
        <style>
        /* ---------- TIPOGRAFIA GLOBAL ---------- */
        html, body, [class*="st-"] {
            font-family: "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }

        /* ---------- TÍTULOS E SUBTÍTULOS ---------- */
        .titulo-principal {
            font-size: 1.8rem;
            font-weight: 700;
            color: #1A1A1A;
            margin-bottom: 0.2rem;
        }
        .subtitulo {
            font-size: 1.05rem;
            color: #4A4A4A;
            opacity: 0.9;
            margin-bottom: 1.2rem;
        }

        /* ---------- FORMULÁRIOS E BLOCOS ---------- */
        label, .stMarkdown, .stTextInput, .stTextArea, .stSelectbox, .stRadio {
            font-size: 0.95rem !important;
        }
        .stTextArea textarea {
            border-radius: 10px !important;
        }

        /* ---------- BOTÕES ---------- */
        .stButton > button {
            background-color: #003366 !important;
            color: #ffffff !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            padding: 0.55rem 1.25rem !important;
            border: none !important;
        }
        .stButton > button:hover {
            background-color: #002a55 !important;
        }

        /* ---------- DIVISORES ---------- */
        hr, .stDivider {
            border-color: #d6d6d6 !important;
            margin-top: 1.2rem !important;
            margin-bottom: 1.2rem !important;
        }

        /* ---------- SIDEBAR ---------- */
        section[data-testid="stSidebar"] {
            background-color: #f8f9fb !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def exibir_cabecalho_padrao(titulo: str, subtitulo: str):
    """
    Exibe o cabeçalho institucional padronizado (sem logo),
    para ser usado no corpo de cada página.
    """
    st.markdown(
        f"""
        <div class="titulo-principal">{titulo}</div>
        <div class="subtitulo">{subtitulo}</div>
        """,
        unsafe_allow_html=True,
    )
