# -*- coding: utf-8 -*-
# =============================================================================
# SynapseNext – SAAB 5.0
# Página: DFD – Formalização da Demanda (vNext)
# =============================================================================

import streamlit as st
from pathlib import Path
import json
import io
import time

# -----------------------------------------------------------------------------
# 🔧 Compatibilidade institucional de caminhos (local + cloud)
# -----------------------------------------------------------------------------
import sys
base_path = Path(__file__).resolve().parents[2]
if str(base_path) not in sys.path:
    sys.path.insert(0, str(base_path))

# ==========================================================
# 📦 Ajuste resiliente para AgentsBridge (DFD)
# ==========================================================
try:
    from utils.agents_bridge import AgentsBridge  # Ambiente local (Codespaces)
except ModuleNotFoundError:
    from streamlit_app.utils.agents_bridge import AgentsBridge  # Streamlit Cloud

# -----------------------------------------------------------------------------
# 📦 Imports adicionais
# -----------------------------------------------------------------------------
try:
    from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
except ModuleNotFoundError:
    from streamlit_app.utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao

try:
    from streamlit_app.utils.integration_dfd import processar_insumo_dfd
except ModuleNotFoundError:
    from utils.integration_dfd import processar_insumo_dfd

# -----------------------------------------------------------------------------
# 🧭 Configuração inicial da página
# -----------------------------------------------------------------------------
st.set_page_config(page_title="DFD – Formalização da Demanda", page_icon="📄", layout="wide")
aplicar_estilo_global()
exibir_cabecalho_padrao("📄 DFD – Formalização da Demanda")

# -----------------------------------------------------------------------------
# 📁 Diretórios principais
# -----------------------------------------------------------------------------
EXPORTS_DIR = Path(__file__).resolve().parents[2] / "exports"
DFD_JSON_PATH = EXPORTS_DIR / "dfd_data.json"

# -----------------------------------------------------------------------------
# ⚙️ Interface principal
# -----------------------------------------------------------------------------
st.markdown("### 🧩 Etapa 1 – Envio do Documento")
arquivo = st.file_uploader("Envie o arquivo de Formalização da Demanda (DFD)", type=["pdf", "docx", "txt"])

if arquivo:
    st.success(f"📄 Arquivo carregado: {arquivo.name}")
    if st.button("⚙️ Processar com IA institucional"):
        with st.spinner("Analisando o documento e extraindo informações..."):
            resultado = processar_insumo_dfd(arquivo)
            if "erro" in resultado:
                st.error(f"Erro: {resultado['erro']}")
            else:
                st.success("✅ Documento processado com sucesso!")
                campos_ai = resultado.get("campos_ai", {})
                st.json(campos_ai)

                # Salva resultado em JSON institucional
                EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
                with open(DFD_JSON_PATH, "w", encoding="utf-8") as f:
                    json.dump(resultado, f, ensure_ascii=False, indent=2)
                st.info(f"💾 Resultado salvo em {DFD_JSON_PATH.name}")

# -----------------------------------------------------------------------------
# 🧠 Etapa 2 – IA Institucional: geração de rascunho
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("### 🤖 Etapa 2 – Geração de Rascunho Inteligente")

if st.button("🧠 Gerar rascunho com IA institucional"):
    with st.spinner("Gerando rascunho de DFD com base no conhecimento institucional..."):
        try:
            agente_dfd = AgentsBridge("DFD")
            resposta = agente_dfd.executar({"acao": "gerar_rascunho"})
            st.text_area("🧾 Rascunho de Formalização da Demanda (IA)", resposta, height=400)
        except Exception as e:
            st.error(f"❌ Falha ao gerar rascunho via IA institucional: {e}")

# -----------------------------------------------------------------------------
# 📤 Etapa 3 – Exportação
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("### 📤 Etapa 3 – Exportar dados processados")

if DFD_JSON_PATH.exists():
    with open(DFD_JSON_PATH, "rb") as f:
        st.download_button("⬇️ Baixar JSON processado", f, file_name="dfd_data.json", mime="application/json")
else:
    st.info("⚠️ Nenhum dado processado ainda. Envie e processe um DFD primeiro.")

# -----------------------------------------------------------------------------
# 🕒 Rodapé técnico
# -----------------------------------------------------------------------------
st.markdown("""
---
<p style='text-align:center;color:#666;font-size:0.9rem'>
DFD – Formalização da Demanda • SynapseNext v5.0 (Institucional)<br>
Ambiente validado em {:%d/%m/%Y %H:%M:%S}
</p>
""".format(time.localtime().tm_year), unsafe_allow_html=True)
