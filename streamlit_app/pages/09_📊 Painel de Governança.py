# ==========================================================
# SynapseNext – Fase Brasília (Passo 11A)
# Painel de Governança — Indicadores e Gráficos Institucionais
# ==========================================================

import sys
from pathlib import Path
from datetime import datetime
import streamlit as st

# Charts
import matplotlib.pyplot as plt

# -----------------------------
# Setup de caminhos e imports
# -----------------------------
current_dir = Path(__file__).resolve().parents[0]
root_dir = current_dir.parents[2] if (current_dir.parents[2] / "utils").exists() else current_dir.parents[1]
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

try:
    from utils.governanca_pipeline import build_governance_snapshot
except Exception as e:
    st.error(f"❌ Erro ao importar governanca_pipeline: {e}")
    st.stop()

# -----------------------------
# Configuração da página
# -----------------------------
st.set_page_config(page_title="SynapseNext — Painel de Governança", layout="wide")
st.title("📊 Painel de Governança — SynapseNext (Fase Brasília)")
st.caption("Indicadores operacionais: Auditoria Digital e Coerência entre Artefatos")

st.divider()
st.subheader("1️⃣ Snapshot Institucional")

# Carrega snapshot
with st.spinner("Carregando indicadores..."):
    snap = build_governance_snapshot()

st.success(f"Snapshot gerado em {snap.get('timestamp')}")

aud = snap.get("auditoria", {})
coe = snap.get("coerencia", {})

cols = st.columns(4)
with cols[0]:
    st.metric("Eventos (auditoria)", value=aud.get("total_eventos", 0))
with cols[1]:
    por_art = aud.get("por_artefato", {})
    st.metric("DFD — eventos", value=por_art.get("DFD", 0))
with cols[2]:
    st.metric("ETP — eventos", value=por_art.get("ETP", 0))
with cols[3]:
    st.metric("TR — eventos", value=por_art.get("TR", 0))

st.divider()
st.subheader("2️⃣ Word Count Médio por Artefato")

wc = aud.get("word_count_medio", {})
artefatos = ["DFD", "ETP", "TR", "Edital"]
valores = [wc.get(a, 0) for a in artefatos]

fig1, ax1 = plt.subplots()
ax1.bar(artefatos, valores)
ax1.set_xlabel("Artefatos")
ax1.set_ylabel("Palavras (média)")
ax1.set_title("Média de palavras nos snapshots auditados")
st.pyplot(fig1)

st.divider()
st.subheader("3️⃣ Últimos Hashes e Snapshots (Auditoria)")

uh = aud.get("ultimo_hash", {})
us = aud.get("ultimo_snapshot", {})
for a in artefatos:
    st.markdown(f"- **{a}** → hash: `{uh.get(a, '') or '—'}` • snapshot: `{us.get(a, '') or '—'}`")

st.divider()
st.subheader("4️⃣ Série Histórica — Coerência Global (Comparador.IA)")

serie = coe.get("serie_coerencia", [])
if serie:
    x = [s.get("stamp", "") for s in serie]
    y = [s.get("coerencia_global", 0) for s in serie]

    fig2, ax2 = plt.subplots()
    ax2.plot(x, y, marker="o")
    ax2.set_xlabel("Data (YYYYMMDD)")
    ax2.set_ylabel("Coerência Global (%)")
    ax2.set_title("Evolução da Coerência Global")
    ax2.grid(True)
    st.pyplot(fig2)
else:
    st.info("Ainda não há relatórios de coerência salvos em `exports/analises/`.")

st.divider()
st.subheader("5️⃣ Últimas Comparações Diretas (Comparador.IA)")

ult_comp = coe.get("ultima_comparacao", {})
if ult_comp:
    for par, v in ult_comp.items():
        st.markdown(f"- **{par}** → Similaridade: `{v}%`")
else:
    st.info("Aguardando geração de relatórios de coerência para exibir comparações.")

st.divider()
st.subheader("6️⃣ Fontes de Dados Carregadas")

fontes = snap.get("fontes", {})
st.markdown("**Arquivos de Auditoria (JSONL):**")
if fontes.get("auditoria_files"):
    st.code("\n".join(fontes["auditoria_files"]))
else:
    st.write("—")

st.markdown("**Relatórios de Coerência (JSON):**")
if fontes.get("analise_files"):
    st.code("\n".join(fontes["analise_files"]))
else:
    st.write("—")

st.caption("SynapseNext • SAAB 5.0 • TJSP — Fase Brasília (vNext)")
