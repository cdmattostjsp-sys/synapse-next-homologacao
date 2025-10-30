# -*- coding: utf-8 -*-
"""
📊 Painel de Governança – SynapseNext vNext+
==============================================================
Consolidação institucional de auditorias e alertas técnicos.
Integração direta com utils.alertas_pipeline.

Versão: vNext+ (SAAB/TJSP)
--------------------------------------------------------------
Este painel apresenta uma visão consolidada da integridade documental,
baseando-se nos alertas gerados automaticamente pela camada de auditoria
semântica e de coerência do SynapseNext.

Autor: Equipe Synapse.Engineer
Instituição: Secretaria de Administração e Abastecimento – TJSP
==============================================================
"""

import streamlit as st
import pandas as pd
from utils.alertas_pipeline import gerar_alertas, export_alerts_json

# ==========================================================
# ⚙️ Configuração inicial
# ==========================================================
st.set_page_config(
    page_title="📊 Painel de Governança – SynapseNext vNext",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Painel de Governança – SynapseNext vNext")
st.caption("Consolidação institucional de auditorias e alertas técnicos (SAAB/TJSP)")

st.divider()

# ==========================================================
# 🧩 Carregamento de dados
# ==========================================================
try:
    alertas = gerar_alertas()
except Exception as e:
    st.error(f"Erro ao carregar alertas: {e}")
    st.stop()

if not alertas or len(alertas) == 0:
    st.warning("Nenhum alerta disponível. Gere alertas no módulo ⚠️ *Alertas Proativos*.")
    st.stop()

# Convertendo em DataFrame
df = pd.DataFrame(alertas)

# ==========================================================
# 🎛️ Filtros dinâmicos
# ==========================================================
st.sidebar.header("⚙️ Filtros de Visualização")

col1, col2 = st.sidebar.columns(2)
with col1:
    severidade_opts = sorted(df["severidade"].unique())
with col2:
    area_opts = sorted(df["area"].unique())

severidade = st.sidebar.multiselect(
    "Filtrar por Severidade",
    options=severidade_opts,
    default=severidade_opts
)

area = st.sidebar.multiselect(
    "Filtrar por Área",
    options=area_opts,
    default=area_opts
)

# Aplicar filtros
df_filtrado = df[(df["severidade"].isin(severidade)) & (df["area"].isin(area))]

# ==========================================================
# 📈 Indicadores de Governança
# ==========================================================
st.subheader("📈 Indicadores de Governança Documental")

colA, colB, colC, colD = st.columns(4)
colA.metric("Total de Alertas", len(df_filtrado))
colB.metric("Alta Severidade", len(df_filtrado[df_filtrado["severidade"] == "alto"]))
colC.metric("Média Severidade", len(df_filtrado[df_filtrado["severidade"] == "medio"]))
colD.metric("Baixa Severidade", len(df_filtrado[df_filtrado["severidade"] == "baixo"]))

# ==========================================================
# 📊 Gráficos e Visualizações
# ==========================================================
st.divider()
st.subheader("📊 Distribuição de Alertas por Severidade")

chart_data = (
    df_filtrado["severidade"]
    .value_counts()
    .rename_axis("Severidade")
    .reset_index(name="Quantidade")
)

st.bar_chart(chart_data, x="Severidade", y="Quantidade")

# ==========================================================
# 🧾 Tabela consolidada de alertas
# ==========================================================
st.divider()
st.subheader("📋 Lista Consolidada de Alertas")

# Garantir que coluna 'severidade' exista
if "severidade" not in df_filtrado.columns:
    st.warning("Coluna 'severidade' ausente nos dados — adicionando valor padrão.")
    df_filtrado["severidade"] = "não classificado"

# Ordenar de forma segura
try:
    df_exibicao = df_filtrado.sort_values(
        by="severidade",
        ascending=False,
        na_position="last"
    )
except Exception:
    df_exibicao = df_filtrado.copy()

with st.expander("🧠 Exibir Detalhamento dos Alertas", expanded=True):
    colunas_base = ["titulo", "area", "status", "mensagem", "recomendacao", "timestamp"]
    colunas_existentes = [c for c in colunas_base if c in df_exibicao.columns]
    st.dataframe(
        df_exibicao[colunas_existentes],
        use_container_width=True,
        hide_index=True,
    )

# ==========================================================
# 💾 Exportação institucional
# ==========================================================
st.divider()
st.subheader("📤 Exportação de Dados")

if st.button("💾 Exportar Alertas Consolidados para JSON"):
    try:
        export_alerts_json({"alerts": alertas})
        st.success("✅ Arquivo JSON exportado com sucesso para a pasta /exports/analises.")
    except Exception as e:
        st.error(f"Erro ao exportar alertas: {e}")

# ==========================================================
# 🏛️ Rodapé institucional
# ==========================================================
st.markdown(
    """
    ---
    **Sistema SynapseNext vNext+**  
    Secretaria de Administração e Abastecimento – Tribunal de Justiça do Estado de São Paulo (SAAB/TJSP)
    """
)
