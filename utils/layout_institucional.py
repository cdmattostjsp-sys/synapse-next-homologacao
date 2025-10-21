# ==========================================================
# 🏛️ SynapseNext – Layout Institucional (versão refinada)
# Correção de overflow e corte do título
# ==========================================================

import streamlit as st
from pathlib import Path
import base64

def _carregar_logo_base64(logo_filename: str = "tjsp_logo.png") -> str:
    """
    Converte o arquivo do logo em Base64 para exibição inline.
    Caminho ajustado para /mount/src/synapse-next/assets/tjsp_logo.png
    """
    root_dir = Path(__file__).resolve().parents[2] / "synapse-next"
    logo_path = root_dir / "assets" / logo_filename

    if not logo_path.exists():
        st.warning(f"⚠️ Logo não encontrado em: {logo_path}")
        return ""
    with open(logo_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


def exibir_cabecalho_institucional(
    titulo: str,
    subtitulo: str,
    logo_filename: str = "tjsp_logo.png"
):
    """
    Exibe o cabeçalho institucional com alinhamento refinado.
    Evita corte superior e mantém estética TJSP.
    """
    logo_base64 = _carregar_logo_base64(logo_filename)

    st.markdown("""
    <style>
    .cabecalho-tjsp {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        gap: 14px;
        margin-top: 5px;      /* 🟢 Recuo suave: evita corte do título */
        margin-bottom: 0.4rem;
    }
    .cabecalho-tjsp img {
        height: 56px;         /* ligeiramente menor para equilíbrio */
        margin-top: 0;
    }
    .cabecalho-texto {
        display: flex;
        flex-direction: column;
        justify-content: center;
        margin-top: 0;
    }
    .cabecalho-texto h1 {
        font-size: 1.46rem;   /* 🔽 Reduzido levemente */
        font-weight: 700;
        color: #222;
        margin: 0;
        line-height: 1.15;
        padding: 0;
    }
    .cabecalho-texto h2 {
        font-size: 0.90rem;   /* 🔽 Subtítulo ajustado */
        font-weight: 500;
        color: #555;
        margin: 2px 0 0 0;
        line-height: 1.1;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="cabecalho-tjsp">
        <img src="data:image/png;base64,{logo_base64}" alt="TJSP Logo">
        <div class="cabecalho-texto">
            <h1>{titulo}</h1>
            <h2>{subtitulo}</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)


def exibir_rodape_institucional():
    """Rodapé institucional padrão."""
    st.markdown("""
    <hr style="margin-top:2rem; margin-bottom:1rem;">
    <div style="text-align:center; font-size:0.85rem; color:#666;">
        <b>SynapseNext – SAAB 5.0</b> • Tribunal de Justiça de São Paulo<br>
        Secretaria de Administração e Abastecimento (SAAB) – Divisão de Inovação e Governança Digital<br>
        <span style="font-size:0.75rem;">Versão institucional – Outubro/2025</span>
    </div>
    """, unsafe_allow_html=True)
