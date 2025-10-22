# ==========================================================
# ⚠️ SynapseNext – Painel de Alertas Proativos
# Secretaria de Administração e Abastecimento – SAAB 5.0
# ==========================================================

import sys
from pathlib import Path
import streamlit as st
import json

# ==========================================================
# 🔧 Ajuste de path e imports institucionais
# ==========================================================
current_dir = Path(__file__).resolve().parents[0]
root_dir = current_dir.parents[2] if (current_dir.parents[2] / "utils").exists() else current_dir.parents[1]
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

# ==========================================================
# 📦 Importa pipeline de alertas
# ==========================================================
try:
    from utils.alertas_pipeline import evaluate_alerts, export_alerts_json, DEFAULTS
except Exception as e:
    st.set_page_config(page_title="SynapseNext — Alertas", layout="wide")
    st.error(f"❌ Erro ao importar alertas_pipeline: {e}")
    st.stop()

# ==========================================================
# ⚙️ Configuração da página
# ==========================================================
st.set_page_config(page_title="SynapseNext — Alertas Proativos", layout="wide", page_icon="⚠️")

# Importa estilo e cabeçalho global
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
    "Alertas Proativos",
    "Varredura automática com base na Auditoria Digital e nas métricas do Comparador.IA"
)
st.divider()

# ==========================================================
# 🎛️ Parâmetros (sidebar)
# ==========================================================
st.sidebar.header("Parâmetros de Avaliação")
min_cg = st.sidebar.slider("Mínimo Coerência Global (%)", 50, 95, DEFAULTS["min_coerencia_global"], 1)
min_pair = st.sidebar.slider("Mínimo Similaridade Par-a-Par (%)", 50, 95, DEFAULTS["min_pairwise"], 1)
stale_days = st.sidebar.slider("Dias sem novos eventos (staleness)", 1, 30, DEFAULTS["max_staleness_days"], 1)
wc_var = st.sidebar.slider("Variação máxima do tamanho (%)", 5, 80, DEFAULTS["max_wc_change_pct"], 1)

cfg = {
    "min_coerencia_global": min_cg,
    "min_pairwise": min_pair,
    "max_staleness_days": stale_days,
    "max_wc_change_pct": wc_var,
}

# ==========================================================
# 🧠 Execução da análise
# ==========================================================
if st.button("🔎 Recalcular Alertas", type="primary"):
    st.session_state["_recalc"] = True

payload = evaluate_alerts(cfg) if st.session_state.get("_recalc") else evaluate_alerts(cfg)
st.success(f"Análise concluída em **{payload.get('timestamp', '—')}**")

# ==========================================================
# 📈 Métricas Resumidas
# ==========================================================
cols = st.columns(4)
with cols[0]:
    st.metric("Alertas (total)", payload["totais"].get("geral", 0))
with cols[1]:
    st.metric("Severidade Alta", payload["totais"].get("alto", 0))
with cols[2]:
    st.metric("Severidade Média", payload["totais"].get("medio", 0))
with cols[3]:
    st.metric("Severidade Baixa", payload["totais"].get("baixo", 0))

st.divider()

# ==========================================================
# 📋 Lista de alertas detalhada
# ==========================================================
alerts = payload.get("alerts", [])

if not alerts:
    st.success("✅ Nenhum alerta encontrado nas regras atuais.")
else:
    ordem = {"alto": 0, "medio": 1, "baixo": 2}
    alerts_sorted = sorted(alerts, key=lambda a: ordem.get(a.get("severidade", "baixo"), 3))

    st.subheader("📋 Lista de Alertas")
    rows = [
        {
            "Sev.": al.get("severidade"),
            "Área": al.get("area"),
            "Artefato": al.get("artefato"),
            "Título": al.get("titulo"),
            "Detalhe": al.get("detalhe"),
            "Recomendação": al.get("recomendacao"),
            "Quando": al.get("timestamp"),
        }
        for al in alerts_sorted
    ]

    # Tabela compacta
    st.dataframe(rows, use_container_width=True, height=300)

    st.divider()
    if st.button("📤 Exportar alertas (JSON)"):
        path = export_alerts_json(payload)
        st.success(f"Alertas exportados para: `{path}`")

# ==========================================================
# 🧩 Inspeção do JSON completo (opcional)
# ==========================================================
with st.expander("📄 Ver JSON completo do resultado"):
    st.json(payload)

# ==========================================================
# 📘 Rodapé institucional simplificado
# ==========================================================
st.markdown("---")
st.caption("SynapseNext – SAAB 5.0 • Tribunal de Justiça de São Paulo • Secretaria de Administração e Abastecimento (SAAB)")
