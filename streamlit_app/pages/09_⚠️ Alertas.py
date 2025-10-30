# streamlit_app/pages/09_⚠️ Alertas.py
# Página padronizada – SAAB 5.0 | SynapseNext – TJSP
# Preserva compatibilidade com o tema ui_style.py

import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime

# === Configuração inicial ===
st.set_page_config(page_title="⚠️ Alertas – SynapseNext", layout="wide")
from ui_style import apply_global_style  # garante coerência visual
apply_global_style()

# === Cabeçalho institucional ===
st.markdown("""
<div style="text-align:center; padding-top: 0.5rem; padding-bottom: 1.5rem;">
    <h1 style="margin-bottom:0; color:#1a3d6d;">⚠️ Painel de Alertas</h1>
    <p style="color:#4d4d4d; font-size:1rem;">Monitoramento de pendências e inconsistências – SAAB/TJSP</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# === Simulação de dados de exemplo ===
# (na versão real, deve ler de utils/diagnostic_fase3_vNext.py ou exports/)
data = pd.DataFrame({
    "Tipo": ["Crítico", "Médio", "Informativo"],
    "Quantidade": [3, 7, 12],
})

# === Cards de resumo ===
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🚨 Críticos", data.loc[0, "Quantidade"], "Pendências graves")
with col2:
    st.metric("⚠️ Médios", data.loc[1, "Quantidade"], "Atenção necessária")
with col3:
    st.metric("ℹ️ Informativos", data.loc[2, "Quantidade"], "Avisos gerais")

st.markdown("")

# === Gráfico de distribuição ===
fig = px.bar(
    data,
    x="Tipo",
    y="Quantidade",
    color="Tipo",
    text_auto=True,
    title="Distribuição de Alertas por Tipo",
)
fig.update_layout(
    title=dict(x=0.5, font=dict(size=18, color="#1a3d6d")),
    font=dict(size=13),
    height=420,
    showlegend=False,
    margin=dict(l=20, r=20, t=60, b=40),
)
st.plotly_chart(fig, use_container_width=True)

# === Detalhamento dos alertas (exemplo) ===
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

# === Rodapé institucional ===
st.markdown("---")
st.markdown(f"""
<div style="text-align:center; color:#666; font-size:0.85rem; padding-top:0.5rem;">
    SynapseNext – SAAB/TJSP • Plataforma Institucional de Governança • v5.0<br>
    Última atualização: {datetime.now().strftime("%d/%m/%Y %H:%M")}
</div>
""", unsafe_allow_html=True)
