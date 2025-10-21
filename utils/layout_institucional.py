# ==========================================================
# 🏛️ SynapseNext – Layout Institucional
# Secretaria de Administração e Abastecimento (SAAB 5.0)
# ==========================================================

import streamlit as st

def exibir_cabecalho_institucional(titulo: str, subtitulo: str, logo_path: str = "assets/logo_tjsp.png"):
    """
    Exibe o cabeçalho institucional padrão do SynapseNext,
    com logo do TJSP, título e subtítulo ajustados para alinhamento preciso.
    """
    gap_px = 14
    logo_height_px = 60
    text_offset_px = 2  # ajuste vertical fino do texto

    st.markdown(f"""
    <style>
    .cabecalho-tjsp {{
        display: flex;
        align-items: center;
        justify-content: flex-start;
        gap: {gap_px}px;
        margin-top: -4px; /* ligeiro ajuste superior */
        margin-bottom: 1.2rem;
    }}
    .cabecalho-tjsp img {{
        height: {logo_height_px}px;
        margin-top: 0;
    }}
    .cabecalho-texto {{
        display: flex;
        flex-direction: column;
        justify-content: center;
        margin-top: {text_offset_px - 4}px; /* Subiu 4px conforme solicitado */
    }}
    .cabecalho-texto h1 {{
        font-size: 1.55rem;
        font-weight: 700;
        color: #2b2b2b;
        margin: 0;
        line-height: 1.3;
    }}
    .cabecalho-texto h2 {{
        font-size: 0.98rem;
        font-weight: 500;
        color: #555;
        margin-top: 2px; /* menor distância entre título e subtítulo */
    }}
    </style>

    <div class="cabecalho-tjsp">
        <img src="{logo_path}" alt="TJSP Logo">
        <div class="cabecalho-texto">
            <h1>{titulo}</h1>
            <h2>{subtitulo}</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)


def exibir_rodape_institucional():
    """
    Exibe o rodapé institucional padrão.
    """
    st.markdown("""
    <hr style="margin-top:2.5rem; margin-bottom:1rem;">
    <div style="text-align:center; font-size:0.85rem; color:#666;">
        <b>SynapseNext – SAAB 5.0</b> • Tribunal de Justiça de São Paulo<br>
        Secretaria de Administração e Abastecimento (SAAB) – Divisão de Inovação e Governança Digital<br>
        <span style="font-size:0.75rem;">Versão institucional – Outubro/2025</span>
    </div>
    """, unsafe_allow_html=True)
