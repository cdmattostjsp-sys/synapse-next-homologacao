# utils/layout_institucional.py
# ==========================================================
# 🎨 Layout Institucional Unificado – SynapseNext (sem conflito)
# ==========================================================

import streamlit as st
from pathlib import Path
import base64

# Reusa os utilitários globais (NÃO conflita)
from utils.ui_style import aplicar_estilo_institucional
from utils.ui_style import rodape_institucional as _rodape_institucional


def exibir_cabecalho_institucional(
    titulo: str,
    subtitulo: str,
    *,
    logo_rel_path: str = "assets/tjsp_logo.png",
    logo_height_px: int = 70,
    gap_px: int = 18,
    text_offset_px: int = 8
):
    """
    Cabeçalho institucional padrão com alinhamento fino entre logotipo e textos.
    Não conflita com ui_style; usa apenas CSS local.
    """
    logo_path = Path(__file__).resolve().parents[1] / logo_rel_path

    st.markdown(f"""
    <style>
    .cabecalho-tjsp {{
        display: flex;
        align-items: center;
        justify-content: flex-start;
        gap: {gap_px}px;
        margin-top: -4px;              /* leve compensação */
        margin-bottom: 1.4rem;
    }}
    .cabecalho-tjsp img {{
        height: {logo_height_px}px;
        margin-top: 0;
    }}
    .cabecalho-texto {{
        display: flex;
        flex-direction: column;
        justify-content: center;
        margin-top: {text_offset_px}px; /* microajuste do bloco de texto */
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
        margin-top: 4px;
    }}
    </style>
    """, unsafe_allow_html=True)

    if logo_path.exists():
        with open(logo_path, "rb") as img_file:
            logo_b64 = base64.b64encode(img_file.read()).decode("utf-8")
        st.markdown(f"""
        <div class="cabecalho-tjsp">
            <img src="data:image/png;base64,{logo_b64}" alt="Logo TJSP">
            <div class="cabecalho-texto">
                <h1>{titulo}</h1>
                <h2>{subtitulo}</h2>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="cabecalho-tjsp">
            <div class="cabecalho-texto">
                <h1>{titulo}</h1>
                <h2>{subtitulo}</h2>
            </div>
        </div>
        """, unsafe_allow_html=True)


def exibir_rodape_institucional():
    """
    Evita duplicação: delega ao rodapé já definido no ui_style.py
    """
    _rodape_institucional()
