# streamlit_app/pages/Next_100_Painel_Executivo.py
# ==============================================================
# SynapseNext – Fase Brasília (Passo 12B)
# Painel Executivo Interativo – TJSP / SAAB
# ==============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import json
from pathlib import Path

st.set_page_config(page_title="Painel Executivo – SynapseNext", layout="wide")

st.title("📊 Painel Executivo – SynapseNext / SAAB")
st.markdown("Visualização integrada de indicadores, alertas e relatórios institucionais.")

# === Carregar dados ===
base_path = Path(__file__).resolve().parents[2] / "exports"
analises = base_path / "analises"
auditoria = base_path / "auditoria"

def carregar_json(path):
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

governanca = carregar_json(max(analises.glob("relatorio_coerencia_*.json"), default=None) or Path())
alertas = carregar_json(max(analises.glob("alertas_*.json"), default=None) or Path())
insights = carregar_json(max(analises.glob("insights_*.json"), default=None) or Path())

# === Carregar logs de uploads (SharePoint) ===
log_path = auditoria / "upload_log.jsonl"
links_sharepoint = []
if log_path.exists():
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            links_sharepoint.append(json.loads(line.strip()))

# === KPIs de Governança ===
st.subheader("📈 Indicadores de Governança")
if governanca:
    df_gov = pd.DataFrame(list(governanca.get("resumo", {}).items()), columns=["Indicador", "Valor"])
    st.dataframe(df_gov, use_container_width=True)
else:
    st.info("Nenhum dado de governança disponível.")

# === Alertas ===
st.subheader("⚠️ Alertas de Auditoria")
if alertas:
    totais = alertas.get("totais", {})
    fig_alertas = px.bar(
        x=list(totais.keys()),
        y=list(totais.values()),
        color=list(totais.keys()),
        title="Distribuição de Alertas por Severidade",
        color_discrete_sequence=["#c0392b", "#e67e22", "#27ae60"]
    )
    st.plotly_chart(fig_alertas, use_container_width=True)
else:
    st.warning("Nenhum alerta encontrado.")

# === Insights ===
st.subheader("💡 Insights Históricos")
serie = insights.get("coerencia_global_mm", [])
if serie:
    df_insights = pd.DataFrame({"Período": range(1, len(serie)+1), "Coerência": serie})
    fig_insights = px.line(df_insights, x="Período", y="Coerência", markers=True,
                           title="Coerência Global – Média Móvel")
    st.plotly_chart(fig_insights, use_container_width=True)
else:
    st.info("Sem dados de insights para exibir.")

# === Relatórios publicados ===
st.subheader("📂 Relatórios Publicados (SharePoint)")
if links_sharepoint:
    df_links = pd.DataFrame(links_sharepoint)
    df_links["uploaded_at"] = pd.to_datetime(df_links["timestamp"]).dt.strftime("%d/%m/%Y %H:%M")
    st.dataframe(df_links[["uploaded_at", "file", "url"]].rename(
        columns={"uploaded_at": "Data", "file": "Arquivo", "url": "Link SharePoint"}
    ), use_container_width=True)
else:
    st.info("Nenhum relatório publicado ainda.")

# === Download do último PDF ===
ultimo_pdf = max((base_path / "relatorios").glob("relatorio_executivo_*.pdf"), default=None)
if ultimo_pdf and ultimo_pdf.exists():
    with open(ultimo_pdf, "rb") as f:
        st.download_button("📥 Baixar Relatório Executivo (PDF)", f, file_name=ultimo_pdf.name)
else:
    st.warning("Nenhum relatório PDF encontrado.")
