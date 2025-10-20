# ==========================================================
# SynapseNext – Fase Brasília | Passo 11F
# Painel Executivo Institucional – TJSP / SAAB 5.0
# ==========================================================
# Função: Exibir visualmente os resultados consolidados dos módulos:
# governança, alertas e insights históricos, além de permitir
# geração do relatório executivo em PDF.
# ==========================================================

import streamlit as st
from pathlib import Path
import json
from datetime import datetime
import matplotlib.pyplot as plt
import io
from utils.relatorio_executivo_pdf import gerar_relatorio_executivo

# ==========================================================
# 🔧 Funções utilitárias
# ==========================================================

def ensure_exports_structure(root_exports: Path):
    """
    Garante a existência da estrutura de diretórios exports/.
    Caso encontre arquivos com o mesmo nome, remove-os e recria
    as pastas necessárias de forma segura.
    """
    subdirs = ["analises", "relatorios", "auditoria", "logs"]
    for folder in subdirs:
        target = root_exports / folder
        if target.exists() and target.is_file():
            target.unlink()  # remove arquivo que impede criação do diretório
        target.mkdir(parents=True, exist_ok=True)


def carregar_json(path: Path):
    """
    Carrega um arquivo JSON se existir; retorna dicionário vazio caso contrário.
    """
    if not path.exists() or not path.is_file():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# ==========================================================
# 🧭 Interface principal
# ==========================================================

st.set_page_config(
    page_title="Painel Executivo – SynapseNext",
    layout="wide",
    page_icon="📊"
)

st.title("📊 Painel Executivo – SynapseNext")
st.markdown("#### Consolidação Institucional • SAAB 5.0 • Tribunal de Justiça de São Paulo")

# ==========================================================
# 🗂️ Estrutura de diretórios
# ==========================================================

root_exports = Path(__file__).resolve().parents[2] / "exports"
ensure_exports_structure(root_exports)

analises = root_exports / "analises"
relatorios = root_exports / "relatorios"

# ==========================================================
# 📂 Carregamento de dados
# ==========================================================

def carregar_dados():
    governanca_path = max(analises.glob("relatorio_coerencia_*.json"), default=None)
    alertas_path = max(analises.glob("alertas_*.json"), default=None)
    insights_path = max(analises.glob("insights_*.json"), default=None)

    governanca = carregar_json(governanca_path) if governanca_path else {}
    alertas = carregar_json(alertas_path) if alertas_path else {}
    insights = carregar_json(insights_path) if insights_path else {}

    return governanca, alertas, insights

governanca, alertas, insights = carregar_dados()

# ==========================================================
# 📈 Visualização dos dados
# ==========================================================

st.divider()
st.subheader("Indicadores Consolidados")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Documentos Auditados", len(governanca.get("documentos", [])))
with col2:
    st.metric("Alertas Totais", sum(alertas.get("totais", {}).values()))
with col3:
    st.metric("Insights Gerados", len(insights.get("serie_temporal", [])))

# ==========================================================
# 📊 Gráfico – Distribuição de Alertas
# ==========================================================

if alertas.get("totais"):
    st.subheader("Distribuição de Alertas por Severidade")
    fig, ax = plt.subplots()
    ax.bar(
        ["Alto", "Médio", "Baixo"],
        [
            alertas["totais"].get("alto", 0),
            alertas["totais"].get("medio", 0),
            alertas["totais"].get("baixo", 0)
        ],
        color=["#C0392B", "#F1C40F", "#27AE60"]
    )
    ax.set_ylabel("Quantidade")
    ax.set_xlabel("Severidade")
    ax.set_title("Alertas Detectados (Classificação)")
    st.pyplot(fig)
else:
    st.info("Nenhum alerta consolidado disponível no momento.")

# ==========================================================
# 📘 Geração do Relatório Executivo em PDF
# ==========================================================

st.divider()
st.subheader("📘 Relatório Executivo – Exportação em PDF")

if st.button("Gerar Relatório Executivo PDF"):
    if not (governanca or alertas or insights):
        st.warning("⚠️ Não há dados consolidados suficientes para gerar o relatório.")
    else:
        caminho_pdf = gerar_relatorio_executivo(governanca, alertas, insights)
        st.success(f"✅ Relatório gerado com sucesso!\n\n📄 Caminho: `{caminho_pdf}`")

        with open(caminho_pdf, "rb") as f:
            st.download_button(
                label="📥 Baixar Relatório Executivo",
                data=f,
                file_name=Path(caminho_pdf).name,
                mime="application/pdf"
            )

# ==========================================================
# 📅 Rodapé
# ==========================================================
st.divider()
st.caption(f"TJSP • Secretaria de Administração e Abastecimento • Projeto SynapseNext – SAAB 5.0  \nVersão institucional vNext • Gerado em {datetime.now():%d/%m/%Y %H:%M}")
