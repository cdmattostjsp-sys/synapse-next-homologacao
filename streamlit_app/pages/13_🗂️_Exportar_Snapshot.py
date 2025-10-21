# ==========================================================
# 🗂️ SynapseNext – Exportação do Snapshot Institucional
# Secretaria de Administração e Abastecimento – SAAB 5.0
# ==========================================================

import sys
from pathlib import Path
import json
import streamlit as st

# ==========================================================
# 🔧 Setup de caminhos e imports
# ==========================================================
current_dir = Path(__file__).resolve().parents[0]
root_dir = current_dir.parents[2] if (current_dir.parents[2] / "utils").exists() else current_dir.parents[1]
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

try:
    from utils.export_snapshot import export_snapshot_json
except Exception as e:
    st.error(f"❌ Erro ao importar módulo de exportação: {e}")
    st.stop()

# ==========================================================
# ⚙️ Configuração da página
# ==========================================================
st.set_page_config(page_title="SynapseNext — Exportação do Snapshot", layout="wide", page_icon="🗂️")

# ==========================================================
# 🎨 Estilo institucional padronizado
# ==========================================================
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
    "Exportação do Snapshot Institucional",
    "Geração do arquivo JSON consolidado com os indicadores do Painel de Governança"
)
st.divider()

# ==========================================================
# 1️⃣ Ação principal – Gerar snapshot
# ==========================================================
if st.button("📤 Gerar e Exportar Snapshot", type="primary", use_container_width=True):
    with st.spinner("Gerando snapshot consolidado..."):
        try:
            path = export_snapshot_json()
            st.success(f"✅ Snapshot exportado com sucesso para: `{path}`")

            # Preview resumido dos principais dados
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            st.subheader("🔍 Resumo do Snapshot")
            resumo = {
                "Timestamp": data.get("timestamp"),
                "Versão": data.get("versao"),
                "Total de Eventos de Auditoria": data.get("auditoria", {}).get("total_eventos"),
                "Média de Coerência (%)": (
                    sum([p.get("coerencia_global", 0) for p in data.get("coerencia", {}).get("serie_coerencia", [])])
                    / max(1, len(data.get("coerencia", {}).get("serie_coerencia", [])))
                ),
                "Arquivos Considerados": data.get("fontes", {}),
            }
            st.json(resumo)

        except Exception as e:
            st.error(f"❌ Erro ao exportar snapshot: {e}")
else:
    st.info("Clique em **Gerar e Exportar Snapshot** para criar o arquivo consolidado no diretório `exports/analises/`.")

# ==========================================================
# 📘 Rodapé institucional simplificado
# ==========================================================
st.markdown("---")
st.caption(
    "SynapseNext – SAAB 5.0 • Tribunal de Justiça de São Paulo • Secretaria de Administração e Abastecimento (SAAB)  "
    "• Fase Brasília (vNext)"
)
