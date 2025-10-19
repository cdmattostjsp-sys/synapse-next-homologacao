# ==========================================================
# SynapseNext – Fase Brasília (Passo 11D)
# Insights Históricos — Séries e Tendências
# ==========================================================

import sys
from pathlib import Path
import streamlit as st
import matplotlib.pyplot as plt

current_dir = Path(__file__).resolve().parents[0]
root_dir = current_dir.parents[2] if (current_dir.parents[2] / "utils").exists() else current_dir.parents[1]
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

try:
    from utils.insights_pipeline import build_insights, export_insights_json
except Exception as e:
    st.set_page_config(page_title="SynapseNext — Insights", layout="wide")
    st.error(f"❌ Erro ao importar insights_pipeline: {e}")
    st.stop()

st.set_page_config(page_title="SynapseNext — Insights Históricos", layout="wide")
st.title("📈 Insights Históricos — SynapseNext (Fase Brasília)")
st.caption("Tendências a partir da Auditoria Digital e do Comparador.IA")

# ----------------------------------------------------------
# Carregar snapshot de insights
# ----------------------------------------------------------
with st.spinner("Gerando snapshot de insights..."):
    snap = build_insights()

st.success(f"Snapshot gerado em {snap.get('timestamp')}")

st.divider()
st.subheader("1️⃣ Volume de Eventos por Dia (Total)")

vol = snap.get("volume_por_dia", [])
if vol:
    x = [v["day"] for v in vol]
    y = [v["events"] for v in vol]

    fig1, ax1 = plt.subplots()
    ax1.plot(x, y, marker="o")
    ax1.set_xlabel("Data (YYYY-MM-DD)")
    ax1.set_ylabel("Eventos de Auditoria")
    ax1.set_title("Volume de eventos por dia (total)")
    ax1.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig1)
else:
    st.info("Sem eventos de auditoria registrados.")

st.divider()
st.subheader("2️⃣ Volume de Eventos por Artefato")

vol_art = snap.get("volume_por_artefato", {})
if vol_art:
    fig2, ax2 = plt.subplots()
    for artefato, serie in vol_art.items():
        x = [s["day"] for s in serie]
        y = [s["events"] for s in serie]
        if x:
            ax2.plot(x, y, marker="o", label=artefato)
    ax2.set_xlabel("Data (YYYY-MM-DD)")
    ax2.set_ylabel("Eventos de Auditoria")
    ax2.set_title("Eventos por artefato")
    ax2.grid(True)
    ax2.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig2)
else:
    st.info("Sem dados por artefato.")

st.divider()
st.subheader("3️⃣ Coerência Global (Comparador.IA)")

coh = snap.get("coherence_series", [])
coh_ma = snap.get("coherence_ma_series", [])
if coh:
    x = [c["day"] for c in coh]
    y = [c["coerencia_global"] for c in coh]

    fig3, ax3 = plt.subplots()
    ax3.plot(x, y, marker="o")
    ax3.set_xlabel("Data (YYYY-MM-DD)")
    ax3.set_ylabel("Coerência Global (%)")
    ax3.set_title("Evolução da Coerência Global")
    ax3.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig3)

    # Média móvel (janela 3)
    if coh_ma:
        xm = [m["day"] for m in coh_ma]
        ym = [m["ma"] for m in coh_ma]
        fig4, ax4 = plt.subplots()
        ax4.plot(xm, ym, marker="o")
        ax4.set_xlabel("Data (YYYY-MM-DD)")
        ax4.set_ylabel("Coerência Global (Média Móvel, w=3)")
        ax4.set_title("Tendência (Média Móvel)")
        ax4.grid(True)
        plt.xticks(rotation=45)
        st.pyplot(fig4)
else:
    st.info("Sem relatórios de coerência encontrados.")

st.divider()
st.subheader("4️⃣ Tamanho Médio (Word Count) por Artefato")

wc_avg = snap.get("wc_day_avg", {})
if wc_avg:
    fig5, ax5 = plt.subplots()
    for artefato, serie in wc_avg.items():
        x = [s["day"] for s in serie]
        y = [s["avg_wc"] for s in serie]
        if x:
            ax5.plot(x, y, marker="o", label=artefato)
    ax5.set_xlabel("Data (YYYY-MM-DD)")
    ax5.set_ylabel("Tamanho médio (palavras)")
    ax5.set_title("Word Count médio por artefato")
    ax5.grid(True)
    ax5.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig5)
else:
    st.info("Sem estatísticas de tamanho por artefato.")

st.divider()
st.subheader("5️⃣ Variação Recente de Tamanho (últimos 2 snapshots)")

wc_delta_recent = snap.get("wc_delta_recent", {})
rows = []
for art, d in wc_delta_recent.items():
    rows.append({
        "Artefato": art,
        "Prev (pal.)": d.get("prev"),
        "Last (pal.)": d.get("last"),
        "Δ%": d.get("delta_pct"),
    })
st.dataframe(rows, use_container_width=True)

st.divider()
if st.button("📤 Exportar Insights (JSON)"):
    path = export_insights_json(snap)
    st.success(f"Insights exportados para: `{path}`")

st.caption("SynapseNext • SAAB 5.0 • TJSP — Fase Brasília (vNext)")
