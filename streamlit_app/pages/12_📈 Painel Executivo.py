import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# ==========================================================
# 📈 SynapseNext – Painel Executivo (SAAB 5.0)
# Secretaria de Administração e Abastecimento – TJSP
# ==========================================================
# Objetivo:
#   Exibir visão consolidada de desempenho, governança e
#   alertas do ecossistema SynapseNext.
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import sys, os
from pathlib import Path

# ==========================================================
# 🔧 Configuração de ambiente e estilo institucional
# ==========================================================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.ui_style import aplicar_estilo_institucional, rodape_institucional
from utils.alertas_pipeline import gerar_alertas

# ==========================================================
# 🔄 Lazy Loading de módulos pesados
# ==========================================================
def _get_relatorio_executivo():
    """Carrega módulo de relatório sob demanda (lazy loading)."""
    try:
        from utils.relatorio_executivo_pdf import gerar_relatorio_executivo
        return gerar_relatorio_executivo
    except ImportError as e:
        st.warning(f"⚠️ Módulo de relatório PDF indisponível: {e}")
        return None

# ==========================================================
# ⚙️ Configuração da página
# ==========================================================
st.set_page_config(
    page_title="📈 Painel Executivo – SynapseNext",
    layout="wide",
    page_icon="📈"
)
aplicar_estilo_institucional()

# ==========================================================
# 🎯 Cabeçalho institucional
# ==========================================================
st.markdown("""
<div style="text-align:center; padding-top: 0.5rem; padding-bottom: 1.2rem;">
    <h1 style="margin-bottom:0; color:#004A8F;">📈 Painel Executivo</h1>
    <p style="color:#4d4d4d; font-size:1rem;">
        Consolidação Institucional de Indicadores, Alertas e Insights – SAAB/TJSP
    </p>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# ==========================================================
# 🧠 Carregamento de dados
# ==========================================================
try:
    alertas = gerar_alertas()
except Exception as e:
    st.error(f"❌ Erro ao carregar alertas: {e}")
    st.stop()

if not alertas or len(alertas) == 0:
    st.warning("⚠️ Nenhum alerta encontrado. Gere alertas no módulo ⚠️ *Painel de Alertas*.")
    st.stop()

df = pd.DataFrame(alertas)
for col in ["severidade", "area", "titulo", "status", "mensagem", "recomendacao"]:
    if col not in df.columns:
        df[col] = "não classificado"

# ==========================================================
# 📊 Indicadores Executivos
# ==========================================================
st.subheader("📊 Indicadores Executivos Consolidado")

total = len(df)
altos = len(df[df["severidade"] == "alto"])
medios = len(df[df["severidade"] == "medio"])
baixos = len(df[df["severidade"] == "baixo"])
areas = df["area"].nunique()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Alertas Totais", total)
col2.metric("Alta Severidade", altos)
col3.metric("Média Severidade", medios)
col4.metric("Baixa Severidade", baixos)
col5.metric("Áreas Afetadas", areas)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# 📉 Distribuição de Severidade
# ==========================================================
st.subheader("📉 Distribuição de Alertas por Severidade")

dist = (
    df["severidade"]
    .value_counts()
    .rename_axis("Severidade")
    .reset_index(name="Quantidade")
)

if not dist.empty:
    fig = px.bar(
        dist,
        x="Severidade",
        y="Quantidade",
        color="Severidade",
        text_auto=True,
        title="Classificação dos Alertas Detectados",
        color_discrete_sequence=["#E74C3C", "#F1C40F", "#2ECC71"]
    )
    fig.update_layout(
        title=dict(x=0.5, font=dict(size=18, color="#004A8F")),
        font=dict(size=13),
        height=420,
        margin=dict(l=20, r=20, t=60, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Nenhum dado disponível para exibir gráfico de severidade.")

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# 🧭 Insights Executivos
# ==========================================================
st.subheader("🧭 Insights e Recomendações Estratégicas")

if altos > 0:
    st.error("⚠️ Foram detectados alertas de **alta severidade**. Recomenda-se auditoria imediata dos documentos críticos.")
elif medios > 0:
    st.warning("ℹ️ A maioria dos alertas possui severidade **média**. Recomenda-se revisão textual e nova análise de coerência.")
else:
    st.success("✅ Nenhum alerta crítico encontrado. A integridade documental está dentro dos parâmetros aceitáveis.")

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# 🗂️ Distribuição Institucional
# ==========================================================
st.subheader("🏛️ Distribuição Institucional de Alertas")

colA, colB = st.columns(2)
with colA:
    st.markdown("**Distribuição por Área Institucional**")
    dist_area = df["area"].value_counts().rename_axis("Área").reset_index(name="Alertas")
    fig_area = px.bar(
        dist_area,
        x="Área",
        y="Alertas",
        color="Área",
        text_auto=True,
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig_area.update_layout(
        title=dict(x=0.5, font=dict(size=16, color="#004A8F")),
        showlegend=False,
        height=400
    )
    st.plotly_chart(fig_area, use_container_width=True)

with colB:
    st.markdown("**Tipos de Alerta Mais Frequentes**")
    tipos = df["titulo"].value_counts().rename_axis("Tipo de Alerta").reset_index(name="Ocorrências").head(10)
    fig_tipos = px.bar(
        tipos,
        x="Ocorrências",
        y="Tipo de Alerta",
        orientation="h",
        text_auto=True,
        color_discrete_sequence=["#007ACC"]
    )
    fig_tipos.update_layout(
        title=dict(x=0.5, font=dict(size=16, color="#004A8F")),
        height=400,
        margin=dict(l=20, r=20, t=60, b=40)
    )
    st.plotly_chart(fig_tipos, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# 📘 Relatório Executivo – Exportação em PDF
# ==========================================================
st.subheader("📘 Relatório Executivo (Exportação PDF)")

if st.button("📤 Gerar Relatório Executivo em PDF", use_container_width=True):
    gerar_relatorio_fn = _get_relatorio_executivo()
    
    if gerar_relatorio_fn is None:
        st.error("⚠️ Funcionalidade de exportação PDF indisponível. Verifique as dependências.")
        st.stop()
    
    try:
        caminho_pdf = gerar_relatorio_fn({}, {"alertas": alertas}, {})
        with open(caminho_pdf, "rb") as f:
            st.download_button(
                label="📥 Baixar Relatório Executivo",
                data=f,
                file_name=Path(caminho_pdf).name,
                mime="application/pdf"
            )
        st.success("✅ Relatório gerado com sucesso.")
    except Exception as e:
        st.error(f"❌ Erro ao gerar relatório: {e}")

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# 📅 Rodapé institucional
# ==========================================================
rodape_institucional()
