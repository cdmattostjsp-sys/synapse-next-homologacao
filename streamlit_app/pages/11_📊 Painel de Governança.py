# ==========================================================
# 📊 SynapseNext – Painel de Governança
# Secretaria de Administração e Abastecimento – SAAB 5.0
# ==========================================================

import sys
from pathlib import Path
from datetime import datetime
import streamlit as st
import matplotlib.pyplot as plt

# ==========================================================
# 🔧 Ajuste de path e imports institucionais
# ==========================================================
current_dir = Path(__file__).resolve().parents[0]
root_dir = current_dir.parents[2] if (current_dir.parents[2] / "utils").exists() else current_dir.parents[1]
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

try:
    from utils.governanca_pipeline import build_governance_snapshot
except Exception as e:
    st.error(f"❌ Erro ao importar governanca_pipeline: {e}")
    st.stop()

# ==========================================================
# ⚙️ Configuração da página
# ==========================================================
st.set_page_config(page_title="SynapseNext — Painel de Governança", layout="wide", page_icon="📊")

# Importa estilo global
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
    "Painel de Governança",
    "Indicadores estratégicos e métricas institucionais — Auditoria Digital e Comparador.IA"
)
st.divider()

# ==========================================================
# 1️⃣ Snapshot Institucional
# ==========================================================
with st.spinner("Carregando indicadores..."):
    snap = build_governance_snapshot()

st.success(f"Snapshot gerado em **{snap.get('timestamp', '—')}**")

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

# ==========================================================
# 2️⃣ Word Count Médio por Artefato
# ==========================================================
st.divider()
st.subheader("2️⃣ Word Count Médio por Artefato")

wc = aud.get("word_count_medio", {})
artefatos = ["DFD", "ETP", "TR", "Edital"]
valores = [wc.get(a, 0) for a in artefatos]

fig1, ax1 = plt.subplots(figsize=(5, 3))
ax1.bar(artefatos, valores, color="#b22222")
ax1.set_xlabel("Artefatos", fontsize=9)
ax1.set_ylabel("Palavras (média)", fontsize=9)
ax1.set_title("Média de palavras nos snapshots auditados", fontsize=10, pad=8)
ax1.grid(axis="y", linestyle="--", alpha=0.5)
st.pyplot(fig1, use_container_width=False)

# ==========================================================
# 3️⃣ Últimos Hashes e Snapshots (Auditoria)
# ==========================================================
st.divider()
st.subheader("3️⃣ Últimos Hashes e Snapshots (Auditoria)")

uh = aud.get("ultimo_hash", {})
us = aud.get("ultimo_snapshot", {})
for a in artefatos:
    st.markdown(f"- **{a}** → hash: `{uh.get(a, '') or '—'}` • snapshot: `{us.get(a, '') or '—'}`")

# ==========================================================
# 4️⃣ Série Histórica — Coerência Global
# ==========================================================
st.divider()
st.subheader("4️⃣ Série Histórica — Coerência Global (Comparador.IA)")

serie = coe.get("serie_coerencia", [])
if serie:
    x = [s.get("stamp", "") for s in serie]
    y = [s.get("coerencia_global", 0) for s in serie]
    fig2, ax2 = plt.subplots(figsize=(6, 3))
    ax2.plot(x, y, marker="o", color="#004b8d", linewidth=1.6)
    ax2.set_xlabel("Data (YYYYMMDD)", fontsize=9)
    ax2.set_ylabel("Coerência Global (%)", fontsize=9)
    ax2.set_title("Evolução da Coerência Global", fontsize=10, pad=8)
    ax2.grid(True, linestyle="--", alpha=0.5)
    plt.xticks(rotation=45, fontsize=8)
    plt.yticks(fontsize=8)
    st.pyplot(fig2, use_container_width=False)
else:
    st.info("Ainda não há relatórios de coerência em `exports/analises/`.")

# ==========================================================
# 5️⃣ Últimas Comparações Diretas
# ==========================================================
st.divider()
st.subheader("5️⃣ Últimas Comparações Diretas (Comparador.IA)")

ult_comp = coe.get("ultima_comparacao", {})
if ult_comp:
    for par, v in ult_comp.items():
        st.markdown(f"- **{par}** → Similaridade: `{v}%`")
else:
    st.info("Aguardando geração de relatórios de coerência.")

# ==========================================================
# 6️⃣ Fontes de Dados Carregadas
# ==========================================================
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

# ==========================================================
# 📘 Rodapé institucional simplificado
# ==========================================================
st.markdown("---")
st.caption("SynapseNext – SAAB 5.0 • Tribunal de Justiça de São Paulo • Secretaria de Administração e Abastecimento (SAAB)")
