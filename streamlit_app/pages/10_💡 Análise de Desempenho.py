import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# ==========================================================
# 💡 SynapseNext – Painel de Análise de Desempenho (SAAB 5.0)
# Secretaria de Administração e Abastecimento – TJSP
# ==========================================================
# Objetivo:
#   Exibir métricas de desempenho técnico e consistência
#   documental com visual padronizado SAAB 5.0.
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import sys, os

# ==========================================================
# 🔧 Configuração de ambiente e estilo institucional
# ==========================================================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.ui_style import aplicar_estilo_institucional, rodape_institucional

st.set_page_config(page_title="💡 Análise de Desempenho – SynapseNext", layout="wide")
aplicar_estilo_institucional()

# ==========================================================
# 🎯 Cabeçalho institucional
# ==========================================================
st.markdown("""
<div style="text-align:center; padding-top: 0.5rem; padding-bottom: 1.2rem;">
    <h1 style="margin-bottom:0; color:#004A8F;">💡 Análise de Desempenho</h1>
    <p style="color:#4d4d4d; font-size:1rem;">Indicadores técnicos e métricas institucionais – SAAB/TJSP</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================================================
# 🧠 Carregamento de dados (simulado)
# ==========================================================
# Na versão real, substituir por dados vindos de utils/insights_pipeline.py
try:
    # Simulação de snapshot de desempenho
    df_volume = pd.DataFrame({
        "data": pd.date_range("2025-10-01", periods=7),
        "valor": [120, 135, 140, 160, 175, 190, 210]
    })

    df_art = pd.DataFrame({
        "data": pd.date_range("2025-10-01", periods=7),
        "DFD": [40, 42, 45, 47, 49, 51, 55],
        "ETP": [30, 34, 36, 39, 40, 44, 46],
        "TR": [25, 27, 28, 31, 33, 35, 37]
    })

    df_coer = pd.DataFrame({
        "data": pd.date_range("2025-10-01", periods=7),
        "valor": [68, 70, 73, 75, 77, 80, 82]
    })

    df_wc = pd.DataFrame({
        "data": pd.date_range("2025-10-01", periods=7),
        "valor": [950, 970, 1000, 1020, 1040, 1060, 1080]
    })

    df_delta = pd.DataFrame({
        "Indicador": ["DFD", "ETP", "TR", "EDITAL"],
        "Variação (%)": [+5.4, +3.8, +4.1, +2.7]
    })
except Exception as e:
    st.error(f"❌ Erro ao carregar dados simulados: {e}")
    st.stop()

# ==========================================================
# 📊 Seção 1 – Evolução temporal (Volume total)
# ==========================================================
st.subheader("📈 Evolução temporal – Volume de eventos")

fig_vol = px.line(
    df_volume, x="data", y="valor", markers=True,
    title="Volume total de eventos registrados",
    line_shape="spline"
)
fig_vol.update_layout(
    title=dict(x=0.5, font=dict(size=18, color="#004A8F")),
    font=dict(size=13),
    height=400,
    margin=dict(l=20, r=20, t=60, b=40)
)
st.plotly_chart(fig_vol, use_container_width=True)
st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# 🗂️ Seção 2 – Volume por artefato
# ==========================================================
st.subheader("📁 Distribuição de eventos por artefato")

df_art_long = df_art.melt(id_vars="data", var_name="Artefato", value_name="Eventos")
fig_art = px.line(
    df_art_long, x="data", y="Eventos", color="Artefato", markers=True,
    title="Evolução por Artefato"
)
fig_art.update_layout(
    title=dict(x=0.5, font=dict(size=18, color="#004A8F")),
    font=dict(size=13),
    height=400,
    legend_title_text="Artefato",
    margin=dict(l=20, r=20, t=60, b=40)
)
st.plotly_chart(fig_art, use_container_width=True)
st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# 🧭 Seção 3 – Coerência global
# ==========================================================
st.subheader("🧭 Tendência de coerência global")

fig_coer = px.line(
    df_coer, x="data", y="valor", markers=True, color_discrete_sequence=["#00A86B"],
    title="Índice de Coerência Global (%)"
)
fig_coer.update_layout(
    title=dict(x=0.5, font=dict(size=18, color="#004A8F")),
    yaxis=dict(range=[0, 100]),
    height=400,
    margin=dict(l=20, r=20, t=60, b=40)
)
st.plotly_chart(fig_coer, use_container_width=True)
st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# 📄 Seção 4 – Tamanho médio dos artefatos
# ==========================================================
st.subheader("📄 Evolução do tamanho médio (WordCount)")

fig_wc = px.line(
    df_wc, x="data", y="valor", markers=True, color_discrete_sequence=["#6A0DAD"],
    title="Média de palavras por artefato"
)
fig_wc.update_layout(
    title=dict(x=0.5, font=dict(size=18, color="#004A8F")),
    height=400,
    margin=dict(l=20, r=20, t=60, b=40)
)
st.plotly_chart(fig_wc, use_container_width=True)
st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# 📉 Seção 5 – Delta percentual recente
# ==========================================================
st.subheader("📉 Variação percentual recente (Δ%)")
st.dataframe(df_delta, use_container_width=True, hide_index=True)
st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# 🏛️ Rodapé institucional
# ==========================================================
rodape_institucional()
