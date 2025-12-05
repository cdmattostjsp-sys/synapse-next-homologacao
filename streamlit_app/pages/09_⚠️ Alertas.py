# ==========================================================
# ⚠️ SynapseNext – Painel de Alertas (SAAB 5.0)
# Secretaria de Administração e Abastecimento – TJSP
# ==========================================================
# Objetivo:
#   Exibir alertas institucionais e pendências detectadas
#   nas etapas do fluxo de contratação pública (Lei 14.133/2021).
#   Esta página adota o padrão visual SAAB 5.0 e o tema global.
# ==========================================================

import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime
import sys, os

# ==========================================================
# 🔧 Configuração de ambiente e estilo institucional
# ==========================================================
from utils.ui_style import aplicar_estilo_institucional, rodape_institucional

# Configuração da página Streamlit
st.set_page_config(page_title="⚠️ Alertas – SynapseNext", layout="wide")
aplicar_estilo_institucional()

# ==========================================================
# 🎯 Cabeçalho institucional
# ==========================================================
st.markdown("""
<div style="text-align:center; padding-top: 0.5rem; padding-bottom: 1.2rem;">
    <h1 style="margin-bottom:0; color:#004A8F;">⚠️ Painel de Alertas</h1>
    <p style="color:#4d4d4d; font-size:1rem;">Monitoramento de pendências e inconsistências – SAAB/TJSP</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================================================
# 📊 Dados simulados (substituir por dados reais do diagnostic_fase3_vNext)
# ==========================================================
data = pd.DataFrame({
    "Tipo": ["Crítico", "Médio", "Informativo"],
    "Quantidade": [3, 7, 12],
})

# ==========================================================
# 📌 Cards de resumo
# ==========================================================
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🚨 Críticos", data.loc[0, "Quantidade"], "Pendências graves")
with col2:
    st.metric("⚠️ Médios", data.loc[1, "Quantidade"], "Atenção necessária")
with col3:
    st.metric("ℹ️ Informativos", data.loc[2, "Quantidade"], "Avisos gerais")

st.markdown("")

# ==========================================================
# 📈 Gráfico de distribuição dos alertas
# ==========================================================
fig = px.bar(
    data,
    x="Tipo",
    y="Quantidade",
    color="Tipo",
    text_auto=True,
    title="Distribuição de Alertas por Tipo",
)

fig.update_layout(
    title=dict(x=0.5, font=dict(size=18, color="#004A8F")),
    font=dict(size=13),
    height=420,
    showlegend=False,
    margin=dict(l=20, r=20, t=60, b=40),
)
st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# 🧾 Detalhamento dos alertas ativos
# ==========================================================
st.markdown("### 🔍 Detalhamento dos Alertas Ativos")

alerts = [
    {"tipo": "Crítico", "mensagem": "Arquivo dfd_data.json ausente em exports/.", "data": "2025-10-28"},
    {"tipo": "Médio", "mensagem": "Campos obrigatórios ausentes no ETP (prazo, objeto).", "data": "2025-10-27"},
    {"tipo": "Informativo", "mensagem": "Nova versão de validator_engine_vNext disponível.", "data": "2025-10-26"},
]

for alert in alerts:
    color = "#c0392b" if alert["tipo"] == "Crítico" else "#f39c12" if alert["tipo"] == "Médio" else "#2980b9"
    st.markdown(
        f"""
        <div style="
            background-color:{color}20;
            border-left:6px solid {color};
            border-radius:8px;
            padding:0.8rem 1rem;
            margin-bottom:0.6rem;
        ">
            <strong style="color:{color};">{alert['tipo']}</strong> – {alert['mensagem']}  
            <div style="font-size:0.85rem; color:#666;">{alert['data']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ==========================================================
# 🏛️ Rodapé institucional
# ==========================================================
rodape_institucional()
