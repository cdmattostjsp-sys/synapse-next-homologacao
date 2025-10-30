# -*- coding: utf-8 -*-
"""
10_💡 Análise de Desempenho.py – Painel de Métricas e Insights
===============================================================
Módulo analítico do SynapseNext vNext (TJSP/SAAB).
Exibe indicadores de desempenho técnico e consistência documental
a partir dos snapshots de auditoria e pipelines de governança.

Versão homologada vNext
===============================================================
"""

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# --------------------------------------------------------------
# 🔧 Importação dos componentes e pipelines
# --------------------------------------------------------------
try:
    from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
    from utils.insights_pipeline import build_insights, export_insights
except Exception as e:
    st.error(f"❌ Erro ao carregar pipeline de insights.\n\nDetalhes técnicos: {e}")
    st.info("Verifique se o arquivo `utils/insights_pipeline.py` está presente e funcional.")
    st.stop()

# --------------------------------------------------------------
# ⚙️ Configuração de página
# --------------------------------------------------------------
st.set_page_config(page_title="💡 Análise de Desempenho", layout="wide")
aplicar_estilo_global()
exibir_cabecalho_padrao("💡 Análise de Desempenho", "Indicadores técnicos e métricas institucionais.")

# --------------------------------------------------------------
# 🧠 Execução principal
# --------------------------------------------------------------
st.divider()
st.subheader("📊 Compilando métricas de desempenho...")

try:
    snap = build_insights()
except Exception as e:
    st.error(f"❌ Falha ao gerar insights: {e}")
    st.stop()

# 🔎 Bloqueio preventivo de snapshot vazio
if not snap:
    st.warning("Nenhum dado de auditoria foi encontrado. Execute primeiro o Painel de Governança ou Auditoria para gerar um snapshot.")
    st.stop()

st.success("✅ Snapshot de auditoria carregado com sucesso.")

# --------------------------------------------------------------
# 🧩 Seção 1 – Volume total de eventos
# --------------------------------------------------------------
st.divider()
st.subheader("📈 Evolução temporal – Volume de eventos")

df_volume = pd.DataFrame(snap.get("volume_tempo", []))
if not df_volume.empty:
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(df_volume["data"], df_volume["valor"], marker="o")
    ax.set_title("Volume total de eventos")
    ax.set_xlabel("Data")
    ax.set_ylabel("Eventos")
    st.pyplot(fig)
else:
    st.info("Sem dados de volume temporal disponíveis.")

st.markdown("<br>", unsafe_allow_html=True)

# --------------------------------------------------------------
# 🧩 Seção 2 – Volume por artefato
# --------------------------------------------------------------
st.divider()
st.subheader("📁 Distribuição de eventos por artefato")

df_art = pd.DataFrame(snap.get("volume_por_artefato", []))
if not df_art.empty:
    fig, ax = plt.subplots(figsize=(6, 3))
    for artefato in df_art["artefato"].unique():
        df_f = df_art[df_art["artefato"] == artefato]
        ax.plot(df_f["data"], df_f["valor"], marker="o", label=artefato)
    ax.set_title("Volume por artefato")
    ax.legend()
    st.pyplot(fig)
else:
    st.info("Nenhum dado de artefato disponível.")

st.markdown("<br>", unsafe_allow_html=True)

# --------------------------------------------------------------
# 🧩 Seção 3 – Coerência global
# --------------------------------------------------------------
st.divider()
st.subheader("🧭 Tendência de coerência global")

df_coer = pd.DataFrame(snap.get("coerencia_global", []))
if not df_coer.empty:
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(df_coer["data"], df_coer["valor"], marker="o", color="green")
    ax.set_title("Coerência Global (média móvel)")
    ax.set_xlabel("Data")
    ax.set_ylabel("Índice (%)")
    st.pyplot(fig)
else:
    st.info("Sem dados de coerência global disponíveis.")

st.markdown("<br>", unsafe_allow_html=True)

# --------------------------------------------------------------
# 🧩 Seção 4 – Word Count médio
# --------------------------------------------------------------
st.divider()
st.subheader("📄 Evolução do tamanho médio dos artefatos")

df_wc = pd.DataFrame(snap.get("wordcount", []))
if not df_wc.empty:
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(df_wc["data"], df_wc["valor"], marker="o", color="purple")
    ax.set_title("Tamanho médio (WordCount)")
    ax.set_xlabel("Data")
    ax.set_ylabel("Palavras")
    st.pyplot(fig)
else:
    st.info("Sem dados de Word Count disponíveis.")

st.markdown("<br>", unsafe_allow_html=True)

# --------------------------------------------------------------
# 🧩 Seção 5 – Delta percentual recente
# --------------------------------------------------------------
st.divider()
st.subheader("📉 Variação percentual recente (Δ%)")

df_delta = pd.DataFrame(snap.get("delta_percentual", []))
if not df_delta.empty:
    st.dataframe(df_delta, use_container_width=True, hide_index=True)
else:
    st.info("Sem dados de variação recente disponíveis.")

st.markdown("<br>", unsafe_allow_html=True)

# --------------------------------------------------------------
# 💾 Exportação de resultados
# --------------------------------------------------------------
st.divider()
st.subheader("📤 Exportação dos Insights")

if st.button("📤 Exportar Insights (JSON)", use_container_width=True):
    try:
        path = export_insights(snap)
        st.success(f"✅ Insights exportados com sucesso: `{path}`")
    except Exception as e:
        st.error(f"❌ Erro ao exportar insights: {e}")

st.caption("Sistema SynapseNext vNext – Secretaria de Administração e Abastecimento (SAAB/TJSP)")
