# ==========================================================
# SynapseNext – Fase Brasília (Passo 11B)
# Exportação do Snapshot Institucional
# ==========================================================

import sys
from pathlib import Path
import streamlit as st
import json

current_dir = Path(__file__).resolve().parents[0]
root_dir = current_dir.parents[2] if (current_dir.parents[2] / "utils").exists() else current_dir.parents[1]
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

try:
    from utils.export_snapshot import export_snapshot_json
except Exception as e:
    st.error(f"❌ Erro ao importar módulo de exportação: {e}")
    st.stop()

# -----------------------------
# Configuração da página
# -----------------------------
st.set_page_config(page_title="SynapseNext — Exportação do Snapshot", layout="centered")
st.title("🧭 Exportação do Snapshot Institucional")
st.caption("Geração automática do arquivo JSON consolidado com os indicadores do Painel de Governança.")

st.divider()

if st.button("📤 Gerar e Exportar Snapshot", type="primary"):
    with st.spinner("Gerando snapshot consolidado..."):
        try:
            path = export_snapshot_json()
            st.success(f"Snapshot exportado com sucesso para: `{path}`")

            # Preview dos principais dados
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            st.subheader("🔍 Resumo do Snapshot")
            st.json({
                "timestamp": data.get("timestamp"),
                "versao": data.get("versao"),
                "total_eventos_auditoria": data.get("auditoria", {}).get("total_eventos"),
                "media_coerencia": (
                    sum([p.get("coerencia_global", 0) for p in data.get("coerencia", {}).get("serie_coerencia", [])])
                    / max(1, len(data.get("coerencia", {}).get("serie_coerencia", [])))
                ),
                "arquivos": data.get("fontes", {})
            })

        except Exception as e:
            st.error(f"Erro ao exportar snapshot: {e}")
else:
    st.info("Clique em **Gerar e Exportar Snapshot** para criar o arquivo consolidado no diretório `exports/analises/`.")

st.divider()
st.caption("SynapseNext • SAAB 5.0 • TJSP — Fase Brasília (vNext)")
