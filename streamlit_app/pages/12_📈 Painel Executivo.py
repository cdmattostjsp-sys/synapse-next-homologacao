# -*- coding: utf-8 -*-
"""
📈 Painel Executivo – SynapseNext vNext+
==============================================================
Consolidação institucional de indicadores, alertas e insights
do ecossistema SynapseNext (SAAB/TJSP).

Autor: Equipe Synapse.Engineer
Instituição: Secretaria de Administração e Abastecimento – TJSP
Versão: vNext+ (atualizado para integração total com alertas_pipeline)
==============================================================
"""

import sys, os
from pathlib import Path
from datetime import datetime
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================================
# 🔧 Ajuste de path
# ==========================================================
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if BASE_PATH not in sys.path:
    sys.path.append(BASE_PATH)

# ==========================================================
# 📦 Importações internas
# ==========================================================
try:
    from utils.alertas_pipeline import gerar_alertas
    from utils.relatorio_executivo_pdf import gerar_relatorio_executivo
    from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
except Exception as e:
    st.error(f"❌ Erro ao importar dependências: {e}")
    st.stop()

# ==========================================================
# ⚙️ Configuração da página
# ==========================================================
st.set_page_config(page_title="📈 Painel Executivo – SynapseNext vNext", layout="wide", page_icon="📈")
aplicar_estilo_global()
exibir_cabecalho_padrao(
    "Painel Executivo",
    "Consolidação Institucional – Indicadores, Alertas e Insights do ecossistema SynapseNext (SAAB 5.0)"
)
st.divider()

# ==========================================================
# 📊 Carregamento dos alertas e dados consolidados
# ==========================================================
try:
    alertas = gerar_alertas()
except Exception as e:
    st.error(f"Erro ao carregar alertas: {e}")
    st.stop()

if not alertas or len(alertas) == 0:
    st.warning("⚠️ Nenhum alerta encontrado. Gere alertas no módulo ⚠️ *Alertas Proativos*.")
    st.stop()

# Converter lista de alertas para DataFrame
df = pd.DataFrame(alertas)

# Garantir colunas obrigatórias
for col in ["severidade", "area", "titulo", "status", "mensagem", "recomendacao"]:
    if col not in df.columns:
        df[col] = "não classificado"

# ==========================================================
# 📈 Indicadores Consolidados
# ==========================================================
st.subheader("1️⃣ Indicadores Consolidados")

total_alertas = len(df)
altos = len(df[df["severidade"] == "alto"])
medios = len(df[df["severidade"] == "medio"])
baixos = len(df[df["severidade"] == "baixo"])
areas_afetadas = df["area"].nunique()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Alertas Totais", total_alertas)
col2.metric("Alta Severidade", altos)
col3.metric("Média Severidade", medios)
col4.metric("Baixa Severidade", baixos)
col5.metric("Áreas Afetadas", areas_afetadas)

# ==========================================================
# 📉 Gráfico de Distribuição de Severidade
# ==========================================================
st.divider()
st.subheader("2️⃣ Distribuição de Alertas por Severidade")

dist = (
    df["severidade"]
    .value_counts()
    .rename_axis("Severidade")
    .reset_index(name="Quantidade")
)

if not dist.empty:
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.bar(dist["Severidade"], dist["Quantidade"], color=["#E74C3C", "#F1C40F", "#2ECC71"])
    ax.set_title("Classificação dos Alertas Detectados", fontsize=10)
    ax.set_xlabel("Severidade", fontsize=9)
    ax.set_ylabel("Quantidade", fontsize=9)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    st.pyplot(fig, use_container_width=False)
else:
    st.info("Nenhum dado disponível para exibir gráfico de severidade.")

# ==========================================================
# 🧠 Insights Executivos
# ==========================================================
st.divider()
st.subheader("3️⃣ Insights Executivos – Análise de Contexto")

if altos > 0:
    st.error("⚠️ Foram detectados alertas de alta severidade. Recomendação: auditoria imediata dos documentos críticos.")
elif medios > 0:
    st.warning("ℹ️ A maioria dos alertas possui severidade média. Recomendação: revisão textual e nova análise de coerência.")
else:
    st.success("✅ Nenhum alerta crítico encontrado. A integridade documental está dentro dos parâmetros aceitáveis.")

# ==========================================================
# 🗂️ Distribuição por Área e Tipos de Alerta
# ==========================================================
st.divider()
st.subheader("4️⃣ Distribuição Institucional de Alertas")

colA, colB = st.columns(2)
with colA:
    st.markdown("**Distribuição por Área Institucional**")
    dist_area = df["area"].value_counts().rename_axis("Área").reset_index(name="Alertas")
    st.dataframe(dist_area, use_container_width=True, hide_index=True)

with colB:
    st.markdown("**Principais Tipos de Alerta**")
    top_alertas = df["titulo"].value_counts().rename_axis("Tipo de Alerta").reset_index(name="Ocorrências")
    st.dataframe(top_alertas, use_container_width=True, hide_index=True)

# ==========================================================
# 📘 Relatório Executivo em PDF
# ==========================================================
st.divider()
st.subheader("5️⃣ Relatório Executivo – Exportação em PDF")

if st.button("📘 Gerar Relatório Executivo PDF"):
    try:
        caminho_pdf = gerar_relatorio_executivo({}, {"alertas": alertas}, {})
        with open(caminho_pdf, "rb") as f:
            st.download_button(
                label="📥 Baixar Relatório Executivo",
                data=f,
                file_name=Path(caminho_pdf).name,
                mime="application/pdf"
            )
        st.success("✅ Relatório gerado e pronto para download.")
    except Exception as e:
        st.error(f"Erro ao gerar relatório: {e}")

# ==========================================================
# 📅 Rodapé institucional
# ==========================================================
st.markdown("---")
st.caption(
    f"SynapseNext – SAAB 5.0 • Tribunal de Justiça de São Paulo • Secretaria de Administração e Abastecimento (SAAB)  \n"
    f"Versão institucional vNext+ • Gerado em {datetime.now():%d/%m/%Y %H:%M}"
)
