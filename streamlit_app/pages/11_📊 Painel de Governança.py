# -*- coding: utf-8 -*-
"""
11_📊 Painel de Governança – SynapseNext vNext
==============================================
Supervisão institucional dos módulos da jornada de
contratação pública (Lei 14.133/2021), incluindo:
- Coerência documental e auditoria;
- Métricas de desempenho;
- Alertas institucionais automáticos.

Autor: Synapse.Engineer
Instituição: TJSP / SAAB
Data: 2025-10-30
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime
from pathlib import Path

# ======================================================
# 🧩 Integrações institucionais
# ======================================================
from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
from utils.governanca_pipeline import build_governance_snapshot, export_governance_snapshot
from utils.insights_pipeline import build_insights, export_insights_json
from utils.alertas_pipeline import gerar_alertas, export_alerts_json

# ======================================================
# ⚙️ Configuração da página
# ======================================================
st.set_page_config(
    page_title="📊 Painel de Governança – SynapseNext",
    layout="wide",
    page_icon="📊"
)

aplicar_estilo_global()
exibir_cabecalho_padrao("📊 Painel de Governança", "Supervisão de Integridade e Desempenho Institucional")

st.markdown("---")

# ======================================================
# 🧠 Construção do snapshot de governança
# ======================================================
st.subheader("🧠 Consolidação de Governança")

with st.spinner("Gerando snapshot institucional..."):
    try:
        snapshot = build_governance_snapshot()
        path = export_governance_snapshot(snapshot)
        st.success("✅ Snapshot de governança gerado com sucesso.")
        st.caption(f"📁 Arquivo exportado: `{path}`")
    except Exception as e:
        st.error(f"❌ Erro ao gerar snapshot de governança: {e}")
        snapshot = {}

if snapshot:
    col1, col2, col3 = st.columns(3)
    col1.metric("Coerência Global (%)", f"{snapshot.get('coerencia_global', 0):.2f}")
    col2.metric("Artefatos Processados", snapshot.get("artefatos", 0))
    col3.metric("Última Atualização", snapshot.get("gerado_em", "—"))

st.markdown("---")

# ======================================================
# 💡 Integração com Insights Institucionais
# ======================================================
st.subheader("💡 Análise de Desempenho")

with st.spinner("Consolidando métricas de desempenho..."):
    try:
        insights = build_insights()
        insights_path = export_insights_json(insights)
        st.success("✅ Insights consolidados com sucesso.")
        st.caption(f"📁 Arquivo exportado: `{insights_path}`")
    except Exception as e:
        st.warning(f"⚠️ Falha ao consolidar métricas: {e}")
        insights = {}

if insights:
    df_vol = pd.DataFrame(insights.get("volume_tempo", []))
    if not df_vol.empty:
        st.line_chart(df_vol.set_index("data")["valor"], height=240)

st.markdown("---")

# ======================================================
# ⚠️ Execução automática do Pipeline de Alertas
# ======================================================
st.subheader("⚠️ Alertas Institucionais")

with st.spinner("Analisando consistência e integridade..."):
    try:
        alertas = gerar_alertas(snapshot)
        if alertas:
            st.success(f"{len(alertas)} alertas detectados no sistema.")
        else:
            st.info("Nenhum alerta identificado no momento.")
    except Exception as e:
        st.error(f"❌ Erro ao gerar alertas: {e}")
        alertas = []

if alertas:
    df_alertas = pd.DataFrame(alertas)

    # 💡 Realce visual por severidade
    def _style_severidade(val):
        if val == "alto":
            color = "red"
        elif val == "medio":
            color = "orange"
        else:
            color = "green"
        return f"color: {color}; font-weight: bold;"

    st.dataframe(
        df_alertas[["severidade", "area", "artefato", "mensagem", "recomendacao"]]
        .style.applymap(_style_severidade, subset=["severidade"]),
        use_container_width=True,
        hide_index=True,
    )

    # 📥 Exportação de alertas
    if st.button("💾 Exportar Alertas em JSON"):
        data = {
            "gerado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "alerts": alertas,
        }
        path = export_alerts_json(data)
        st.success(f"Arquivo salvo em: `{path}`")

st.markdown("---")

# ======================================================
# 🧾 Histórico Institucional
# ======================================================
st.subheader("🗂️ Histórico de Snapshots")

exports_dir = Path("exports/analises")
if exports_dir.exists():
    files = sorted(exports_dir.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)
    if files:
        st.dataframe(
            pd.DataFrame(
                [{"Arquivo": f.name, "Modificado em": datetime.fromtimestamp(f.stat().st_mtime).strftime("%d/%m/%Y %H:%M:%S")} for f in files]
            ),
            hide_index=True,
            use_container_width=True,
        )
    else:
        st.info("Nenhum snapshot encontrado.")
else:
    st.info("Diretório de análises ainda não criado.")

st.markdown("---")
st.caption("📊 Painel de Governança – SynapseNext vNext • SAAB / TJSP • Engenharia Institucional")
