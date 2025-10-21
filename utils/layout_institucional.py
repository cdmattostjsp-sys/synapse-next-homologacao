# ==========================================================
# 🏛️ SynapseNext – Layout Institucional (versão ajustada)
# Secretaria de Administração e Abastecimento (SAAB 5.0)
# ==========================================================

import streamlit as st
from pathlib import Path

def exibir_cabecalho_institucional(
    titulo: str,
    subtitulo: str,
    logo_filename: str = "tjsp_logo.png"  # nome corrigido
):
    """
    Exibe o cabeçalho institucional padrão com alinhamento refinado
    e caminho dinâmico para o logo institucional do TJSP.
    """

    # Caminho absoluto do logo — compatível com execução a partir de /utils/ ou /pages/
    root_dir = Path(__file__).resolve().parents[1]
    logo_path = root_dir / "assets" / logo_filename

    if not logo_path.exists():
        st.warning(f"⚠️ Logo não encontrado em: {logo_path}")
        logo_url = ""
    else:
        logo_url = str(logo_path).replace("\\", "/")

    # Estilo visual refinado e ajustado milimetricamente
    st.markdown("""
    <style>
    .cabecalho-tjsp {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        gap: 14px;
        margin-top: 0px;       /* sem deslocamento negativo */
        margin-bottom: 0.8rem; /* distância equilibrada antes do conteúdo */
    }
    .cabecalho-tjsp img {
        height: 64px;          /* proporção ideal para a tipografia */
        margin-top: 0;
    }
    .cabecalho-texto {
        display: flex;
        flex-direction: column;
        justify-content: center;
        margin-top: 0px;
    }
    .cabecalho-texto h1 {
        font-size: 1.52rem;
        font-weight: 700;
        color: #222;
        margin: 0;
        line-height: 1.25;
    }
    .cabecalho-texto h2 {
        font-size: 0.96rem;
        font-weight: 500;
        color: #555;
        margin: 2px 0 0 0;     /* reduzido o espaçamento entre título e subtítulo */
        line-height: 1.2;
    }
    </style>
    """, unsafe_allow_html=True)

    # Renderização do cabeçalho
    st.markdown(f"""
    <div class="cabecalho-tjsp">
        <img src="file://{logo_url}" alt="TJSP Logo">
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
    <hr style="margin-top:2.2rem; margin-bottom:1rem;">
    <div style="text-align:center; font-size:0.85rem; color:#666;">
        <b>SynapseNext – SAAB 5.0</b> • Tribunal de Justiça de São Paulo<br>
        Secretaria de Administração e Abastecimento (SAAB) – Divisão de Inovação e Governança Digital<br>
        <span style="font-size:0.75rem;">Versão institucional – Outubro/2025</span>
    </div>
    """, unsafe_allow_html=True)
