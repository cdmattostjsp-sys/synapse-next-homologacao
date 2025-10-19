# ==============================================================
# SynapseNext – Fase Brasília (Passo 12B)
# Painel Executivo Interativo – TJSP / SAAB
# ==============================================================
# Versão revisada 2025-10-19
# ==============================================================
import streamlit as st
import pandas as pd
import plotly.express as px
import json
from pathlib import Path

# === Configuração da página ===
st.set_page_config(page_title="Painel Executivo – SynapseNext", layout="wide")
st.title("📊 Painel Executivo – SynapseNext / SAAB")
st.markdown("Visualização integrada de indicadores, alertas e relatórios institucionais.")

# === Caminhos padrão ===
base_path = Path(__file__).resolve().parents[2] / "exports"
analises = base_path / "analises"
auditoria = base_path / "auditoria"
relatorios = base_path / "relatorios"

# ==============================================================
# Funções utilitárias
# ==============================================================

def carregar_json(path: Path):
    """
    Carrega um arquivo JSON de forma segura.
    Retorna um dicionário vazio se o arquivo não existir ou for inválido.
    """
    if not path or not path.exists() or path.is_dir():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.warning(f"⚠️ Erro ao carregar {path.name}: {e}")
        return {}

def get_latest_file(pattern: str):
    """
    Retorna o arquivo mais recente dentro de 'exports/analises' que corresponda ao padrão informado.
    """
    files = list(analises.glob(pattern))
    return max(files, key=lambda p: p.stat().st_mtime) if files else None

# ==============================================================
# Verificações iniciais
# ==============================================================

if not analises.exists():
    st.error("❌ Pasta 'exports/analises' não encontrada. Gere os relatórios de análise antes de continuar.")
    st.stop()

# Aviso se não houver arquivos
if not any(analises.glob("*.json")):
    st.warning("Nenhum arquivo de análise encontrado em 'exports/analises/'. Gere os relatórios antes de abrir o Painel Executivo.")
    st.stop()

# ==============================================================
# Carregamento de dados
# ==============================================================

governanca = carregar_json(get_latest_file("relatorio_coerencia_*.json"))
alertas = carregar_json(get_latest_file("alertas_*.json"))
insights = carregar_json(get_latest_file("insights_*.json"))

# ==============================================================
# Seção: Governança
# ==============================================================

st.subheader("📈 Indicadores de Governança")

if governanca:
    resumo = governanca.get("resumo", {})
    if resumo:
        df_gov = pd.DataFrame(list(resumo.items()), columns=["Indicador", "Valor"])
        st.dataframe(df_gov, use_container_width=True)
    else:
        st.info("Nenhum indicador de governança disponível.")
else:
    st.info("Arquivo de governança não encontrado ou vazio.")

# ==============================================================
# Seção: Alertas
# ==============================================================

st.subheader("⚠️ Alertas de Auditoria")

if alertas:
    totais = alertas.get("totais", {})
    if totais:
        fig_alertas = px.bar(
            x=list(totais.keys()),
            y=list(totais.values()),
            color=list(totais.keys()),
            title="Distribuição de Alertas por Severidade",
            color_discrete_sequence=["#c0392b", "#e67e22", "#27ae60"]
        )
        st.plotly_chart(fig_alertas, use_container_width=True)
    else:
        st.info("Nenhum alerta registrado.")
else:
    st.warning("Arquivo de alertas não encontrado.")

# ==============================================================
# Seção: Insights Históricos
# ==============================================================

st.subheader("💡 Insights Históricos")

serie = insights.get("coerencia_global_mm", []) if insights else []
if serie:
    df_insights = pd.DataFrame({"Período": range(1, len(serie) + 1), "Coerência": serie})
    fig_insights = px.line(
        df_insights,
        x="Período",
        y="Coerência",
        markers=True,
        title="Coerência Global – Média Móvel",
        line_shape="spline",
        color_discrete_sequence=["#2c3e50"]
    )
    st.plotly_chart(fig_insights, use_container_width=True)
else:
    st.info("Sem dados de insights disponíveis.")

# ==============================================================
# Seção: Relatórios Publicados (SharePoint)
# ==============================================================

st.subheader("📂 Relatórios Publicados (SharePoint)")

log_path = auditoria / "upload_log.jsonl"
links_sharepoint = []

if log_path.exists():
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                links_sharepoint.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                continue

if links_sharepoint:
    df_links = pd.DataFrame(links_sharepoint)
    if "timestamp" in df_links.columns:
        df_links["uploaded_at"] = pd.to_datetime(df_links["timestamp"], errors="coerce").dt.strftime("%d/%m/%Y %H:%M")
    df_display = df_links.rename(
        columns={"uploaded_at": "Data", "file": "Arquivo", "url": "Link SharePoint"}
    )
    st.dataframe(df_display[["Data", "Arquivo", "Link SharePoint"]], use_container_width=True)
else:
    st.info("Nenhum relatório publicado encontrado.")

# ==============================================================
# Seção: Download do último PDF
# ==============================================================

st.subheader("📄 Último Relatório Executivo Gerado")

ultimo_pdf = max(relatorios.glob("relatorio_executivo_*.pdf"), default=None)
if ultimo_pdf and ultimo_pdf.exists():
    with open(ultimo_pdf, "rb") as f:
        st.download_button(
            label="📥 Baixar Relatório Executivo (PDF)",
            data=f,
            file_name=ultimo_pdf.name,
            mime="application/pdf"
        )
else:
    st.warning("Nenhum relatório PDF encontrado em 'exports/relatorios/'.")
