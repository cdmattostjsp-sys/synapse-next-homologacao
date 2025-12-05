import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# ==========================================================
# 📊 SynapseNext – Painel de Governança (SAAB 5.0)
# Secretaria de Administração e Abastecimento – TJSP
# ==========================================================
# Objetivo:
#   Consolidar auditorias e alertas técnicos institucionais,
#   com visual unificado e responsivo.
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import sys, os

# ==========================================================
# 🔧 Configuração de ambiente e estilo institucional
# ==========================================================
from utils.ui_style import aplicar_estilo_institucional, rodape_institucional
from utils.alertas_pipeline import gerar_alertas, export_alerts_json

st.set_page_config(
    page_title="📊 Painel de Governança – SynapseNext",
    layout="wide"
)
aplicar_estilo_institucional()

# ==========================================================
# 🎯 Cabeçalho institucional
# ==========================================================
st.markdown("""
<div style="text-align:center; padding-top: 0.5rem; padding-bottom: 1.2rem;">
    <h1 style="margin-bottom:0; color:#004A8F;">📊 Painel de Governança</h1>
    <p style="color:#4d4d4d; font-size:1rem;">
        Consolidação institucional de auditorias e alertas técnicos – SAAB/TJSP
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================================================
# 🧩 Carregamento de dados
# ==========================================================
try:
    alertas = gerar_alertas()
except Exception as e:
    st.error(f"❌ Erro ao carregar alertas: {e}")
    st.stop()

if not alertas or len(alertas) == 0:
    st.warning("Nenhum alerta disponível. Gere alertas no módulo ⚠️ *Painel de Alertas*.")
    st.stop()

df = pd.DataFrame(alertas)

# ==========================================================
# 🎛️ Filtros de visualização
# ==========================================================
st.sidebar.header("⚙️ Filtros de Visualização")

col1, col2 = st.sidebar.columns(2)
with col1:
    severidade_opts = sorted(df["severidade"].dropna().unique())
with col2:
    area_opts = sorted(df["area"].dropna().unique())

severidade = st.sidebar.multiselect("Filtrar por Severidade", severidade_opts, default=severidade_opts)
area = st.sidebar.multiselect("Filtrar por Área", area_opts, default=area_opts)

df_filtrado = df[(df["severidade"].isin(severidade)) & (df["area"].isin(area))]

# ==========================================================
# 📈 Indicadores principais
# ==========================================================
st.subheader("📈 Indicadores de Governança Documental")

colA, colB, colC, colD = st.columns(4)
colA.metric("Total de Alertas", len(df_filtrado))
colB.metric("Alta Severidade", len(df_filtrado[df_filtrado["severidade"] == "alto"]))
colC.metric("Média Severidade", len(df_filtrado[df_filtrado["severidade"] == "medio"]))
colD.metric("Baixa Severidade", len(df_filtrado[df_filtrado["severidade"] == "baixo"]))

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# 📊 Distribuição de alertas por severidade
# ==========================================================
st.subheader("📊 Distribuição de Alertas por Severidade")

chart_data = (
    df_filtrado["severidade"]
    .value_counts()
    .rename_axis("Severidade")
    .reset_index(name="Quantidade")
)

if not chart_data.empty:
    fig = px.bar(
        chart_data,
        x="Severidade",
        y="Quantidade",
        color="Severidade",
        text_auto=True,
        title="Distribuição de Alertas por Severidade",
        color_discrete_sequence=["#c0392b", "#f39c12", "#2980b9"]
    )
    fig.update_layout(
        title=dict(x=0.5, font=dict(size=18, color="#004A8F")),
        font=dict(size=13),
        height=420,
        margin=dict(l=20, r=20, t=60, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Nenhum dado disponível para o gráfico de severidade.")

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# 🧾 Tabela consolidada de alertas
# ==========================================================
st.subheader("📋 Lista Consolidada de Alertas")

if "severidade" not in df_filtrado.columns:
    df_filtrado["severidade"] = "não classificado"

try:
    df_exibicao = df_filtrado.sort_values(by="severidade", ascending=False, na_position="last")
except Exception:
    df_exibicao = df_filtrado.copy()

colunas_base = ["titulo", "area", "status", "mensagem", "recomendacao", "timestamp"]
colunas_existentes = [c for c in colunas_base if c in df_exibicao.columns]

with st.expander("🧠 Exibir Detalhamento dos Alertas", expanded=True):
    st.dataframe(df_exibicao[colunas_existentes], use_container_width=True, hide_index=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# 💾 Exportação institucional
# ==========================================================
st.subheader("📤 Exportação de Dados")

if st.button("💾 Exportar Alertas Consolidados para JSON", use_container_width=True):
    try:
        export_alerts_json({"alerts": alertas})
        st.success("✅ Arquivo JSON exportado com sucesso para a pasta /exports/analises.")
    except Exception as e:
        st.error(f"❌ Erro ao exportar alertas: {e}")

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# 🏛️ Rodapé institucional
# ==========================================================
rodape_institucional()
