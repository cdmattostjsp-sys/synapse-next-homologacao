# ==========================================================
# 📈 SynapseNext – Painel Executivo
# Secretaria de Administração e Abastecimento – SAAB 5.0
# ==========================================================

import streamlit as st
import sys
from pathlib import Path
import json
from datetime import datetime
import matplotlib.pyplot as plt

# ==========================================================
# 🔧 Ajuste de path
# ==========================================================
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# ==========================================================
# 📦 Importações internas
# ==========================================================
try:
    from utils.relatorio_executivo_pdf import gerar_relatorio_executivo
except Exception as e:
    st.error(f"❌ Erro ao importar módulo de relatório: {e}")
    st.stop()

try:
    from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
except Exception:
    aplicar_estilo_global = lambda: None
    exibir_cabecalho_padrao = lambda *a, **kw: None

# ==========================================================
# ⚙️ Configuração da página
# ==========================================================
st.set_page_config(page_title="Painel Executivo – SynapseNext", layout="wide", page_icon="📈")
aplicar_estilo_global()

# ==========================================================
# 🏛️ Cabeçalho institucional padronizado
# ==========================================================
exibir_cabecalho_padrao(
    "Painel Executivo",
    "Consolidação Institucional – Indicadores, Alertas e Insights do ecossistema SynapseNext (SAAB 5.0)"
)
st.divider()

# ==========================================================
# 🗂️ Estrutura e carregamento de dados
# ==========================================================
def ensure_exports_structure(root_exports: Path):
    """Garante a estrutura de diretórios exports/"""
    subdirs = ["analises", "relatorios", "auditoria", "logs"]
    for folder in subdirs:
        target = root_exports / folder
        if target.exists() and target.is_file():
            target.unlink()
        target.mkdir(parents=True, exist_ok=True)

def carregar_json(path: Path):
    """Carrega um arquivo JSON se existir"""
    if not path or not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

root_exports = ROOT_DIR / "exports"
ensure_exports_structure(root_exports)

analises = root_exports / "analises"
relatorios = root_exports / "relatorios"

def carregar_dados():
    governanca_path = max(analises.glob("relatorio_coerencia_*.json"), default=None)
    alertas_path = max(analises.glob("alertas_*.json"), default=None)
    insights_path = max(analises.glob("insights_*.json"), default=None)

    governanca = carregar_json(governanca_path)
    alertas = carregar_json(alertas_path)
    insights = carregar_json(insights_path)
    return governanca, alertas, insights

governanca, alertas, insights = carregar_dados()

# ==========================================================
# 📊 Indicadores Consolidados
# ==========================================================
st.subheader("1️⃣ Indicadores Consolidados")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Documentos Auditados", len(governanca.get("documentos", [])))
with col2:
    st.metric("Alertas Totais", sum(alertas.get("totais", {}).values()))
with col3:
    st.metric("Insights Gerados", len(insights.get("serie_temporal", [])))

# ==========================================================
# 📈 Distribuição de Alertas por Severidade
# ==========================================================
st.divider()
st.subheader("2️⃣ Distribuição de Alertas por Severidade")

if alertas.get("totais"):
    fig, ax = plt.subplots(figsize=(5, 3))
    severidades = ["Alto", "Médio", "Baixo"]
    valores = [
        alertas["totais"].get("alto", 0),
        alertas["totais"].get("medio", 0),
        alertas["totais"].get("baixo", 0),
    ]
    cores = ["#C0392B", "#F1C40F", "#27AE60"]
    ax.bar(severidades, valores, color=cores)
    ax.set_xlabel("Severidade", fontsize=9)
    ax.set_ylabel("Quantidade", fontsize=9)
    ax.set_title("Classificação dos Alertas Detectados", fontsize=10, pad=8)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    st.pyplot(fig, use_container_width=False)
else:
    st.info("Nenhum alerta consolidado disponível no momento.")

# ==========================================================
# 🧭 Síntese dos Principais Dados
# ==========================================================
st.divider()
st.subheader("3️⃣ Síntese dos Principais Dados")

st.markdown("""
- **Governança** → Indicadores de coerência e auditoria digital.
- **Alertas** → Sinais de inconsistência ou comportamento anômalo.
- **Insights** → Tendências históricas e variações percentuais.
""")

if not (governanca or alertas or insights):
    st.warning("⚠️ Nenhum dado disponível. Gere relatórios antes de usar este painel.")
else:
    st.success("✅ Dados carregados com sucesso e prontos para consolidação.")

# ==========================================================
# 📘 Geração do Relatório Executivo em PDF
# ==========================================================
st.divider()
st.subheader("4️⃣ Relatório Executivo – Exportação em PDF")

if st.button("📘 Gerar Relatório Executivo PDF"):
    if not (governanca or alertas or insights):
        st.warning("⚠️ Não há dados consolidados suficientes para gerar o relatório.")
    else:
        caminho_pdf = gerar_relatorio_executivo(governanca, alertas, insights)
        st.success("✅ Relatório gerado com sucesso!")

        with open(caminho_pdf, "rb") as f:
            st.download_button(
                label="📥 Baixar Relatório Executivo",
                data=f,
                file_name=Path(caminho_pdf).name,
                mime="application/pdf"
            )

# ==========================================================
# 📅 Rodapé institucional
# ==========================================================
st.markdown("---")
st.caption(
    f"SynapseNext – SAAB 5.0 • Tribunal de Justiça de São Paulo • Secretaria de Administração e Abastecimento (SAAB)  \n"
    f"Versão institucional vNext • Gerado em {datetime.now():%d/%m/%Y %H:%M}"
)
