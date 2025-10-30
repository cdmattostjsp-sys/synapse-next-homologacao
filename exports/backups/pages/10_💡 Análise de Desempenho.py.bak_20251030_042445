# ==========================================================
# 💡 SynapseNext – Insights Históricos
# Secretaria de Administração e Abastecimento – SAAB 5.0
# ==========================================================

import sys
from pathlib import Path
import streamlit as st
import matplotlib.pyplot as plt

# ==========================================================
# 🔧 Ajuste de path e imports institucionais
# ==========================================================
current_dir = Path(__file__).resolve().parents[0]
root_dir = current_dir.parents[2] if (current_dir.parents[2] / "utils").exists() else current_dir.parents[1]
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

# ==========================================================
# 📦 Importa pipeline de insights
# ==========================================================
try:
    from utils.insights_pipeline import build_insights, export_insights_json
except Exception as e:
    st.set_page_config(page_title="SynapseNext — Insights", layout="wide")
    st.error(f"❌ Erro ao importar insights_pipeline: {e}")
    st.stop()

# ==========================================================
# ⚙️ Configuração da página
# ==========================================================
st.set_page_config(page_title="SynapseNext — Insights Históricos", layout="wide", page_icon="💡")

# Importa estilo global padronizado
try:
    from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
except Exception:
    aplicar_estilo_global = lambda: None
    exibir_cabecalho_padrao = lambda *a, **kw: None

aplicar_estilo_global()

# ==========================================================
# 🏛️ Cabeçalho institucional padronizado
# ==========================================================
exibir_cabecalho_padrao(
    "Insights Históricos",
    "Painel analítico – tendências e métricas derivadas da Auditoria Digital e Comparador.IA"
)
st.divider()

# ==========================================================
# 📊 Carregamento de dados
# ==========================================================
with st.spinner("Gerando snapshot de insights..."):
    snap = build_insights()

st.success(f"Snapshot gerado em {snap.get('timestamp')}")

# ==========================================================
# 🔹 Função auxiliar para criar gráficos compactos
# ==========================================================
def plot_compacto(title, xlabel, ylabel, x, y_dict, legend=True):
    """Gera gráfico com estilo compacto e legível."""
    fig, ax = plt.subplots(figsize=(6, 3))  # tamanho reduzido
    for label, y in y_dict.items():
        ax.plot(x, y, marker="o", linewidth=1.5, label=label)
    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.set_title(title, fontsize=10, pad=8)
    ax.grid(True, linestyle="--", alpha=0.5)
    plt.xticks(rotation=45, fontsize=8)
    plt.yticks(fontsize=8)
    if legend:
        ax.legend(fontsize=8, loc="best")
    st.pyplot(fig, use_container_width=False)

# ==========================================================
# 1️⃣ Volume de Eventos por Dia (Total)
# ==========================================================
st.subheader("1️⃣ Volume de Eventos por Dia (Total)")

vol = snap.get("volume_por_dia", [])
if vol:
    x = [v["day"] for v in vol]
    y = [v["events"] for v in vol]
    plot_compacto("Volume de eventos por dia (total)", "Data (YYYY-MM-DD)", "Eventos de Auditoria", x, {"Total": y})
else:
    st.info("Sem eventos de auditoria registrados.")

# ==========================================================
# 2️⃣ Volume de Eventos por Artefato
# ==========================================================
st.divider()
st.subheader("2️⃣ Volume de Eventos por Artefato")

vol_art = snap.get("volume_por_artefato", {})
if vol_art:
    for artefato, serie in vol_art.items():
        x = [s["day"] for s in serie]
        y = [s["events"] for s in serie]
        plot_compacto(f"Eventos – {artefato}", "Data (YYYY-MM-DD)", "Eventos", x, {artefato: y}, legend=False)
else:
    st.info("Sem dados por artefato.")

# ==========================================================
# 3️⃣ Coerência Global (Comparador.IA)
# ==========================================================
st.divider()
st.subheader("3️⃣ Coerência Global (Comparador.IA)")

coh = snap.get("coherence_series", [])
coh_ma = snap.get("coherence_ma_series", [])
if coh:
    x = [c["day"] for c in coh]
    y = [c["coerencia_global"] for c in coh]
    plot_compacto("Evolução da Coerência Global (%)", "Data (YYYY-MM-DD)", "Coerência (%)", x, {"Coerência": y}, legend=False)

    if coh_ma:
        xm = [m["day"] for m in coh_ma]
        ym = [m["ma"] for m in coh_ma]
        plot_compacto("Tendência (Média Móvel w=3)", "Data (YYYY-MM-DD)", "Coerência (Média Móvel)", xm, {"Média móvel": ym}, legend=False)
else:
    st.info("Sem relatórios de coerência encontrados.")

# ==========================================================
# 4️⃣ Tamanho Médio (Word Count) por Artefato
# ==========================================================
st.divider()
st.subheader("4️⃣ Tamanho Médio (Word Count) por Artefato")

wc_avg = snap.get("wc_day_avg", {})
if wc_avg:
    for artefato, serie in wc_avg.items():
        x = [s["day"] for s in serie]
        y = [s["avg_wc"] for s in serie]
        plot_compacto(f"Tamanho médio – {artefato}", "Data (YYYY-MM-DD)", "Palavras", x, {artefato: y}, legend=False)
else:
    st.info("Sem estatísticas de tamanho por artefato.")

# ==========================================================
# 5️⃣ Variação Recente de Tamanho (últimos snapshots)
# ==========================================================
st.divider()
st.subheader("5️⃣ Variação Recente de Tamanho (últimos snapshots)")

wc_delta_recent = snap.get("wc_delta_recent", {})
rows = []
for art, d in wc_delta_recent.items():
    rows.append({
        "Artefato": art,
        "Prev (pal.)": d.get("prev"),
        "Last (pal.)": d.get("last"),
        "Δ%": d.get("delta_pct"),
    })
st.dataframe(rows, use_container_width=True, height=240)

# ==========================================================
# 📤 Exportação
# ==========================================================
st.divider()
if st.button("📤 Exportar Insights (JSON)"):
    path = export_insights_json(snap)
    st.success(f"Insights exportados para: `{path}`")

# ==========================================================
# 📘 Rodapé institucional simplificado
# ==========================================================
st.markdown("---")
st.caption("SynapseNext – SAAB 5.0 • Tribunal de Justiça de São Paulo • Secretaria de Administração e Abastecimento (SAAB)")
