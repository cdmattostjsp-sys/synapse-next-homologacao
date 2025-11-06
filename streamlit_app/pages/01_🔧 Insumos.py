# ==========================================================
# pages/01_🔧 Insumos.py
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# Revisão: Engenheiro Synapse – INC-2025-11-05-INSUMOS-UPLOAD (versão saneada)
# ==========================================================

import os
import json
import streamlit as st
from pathlib import Path

# ==========================================================
# 📦 Imports institucionais (padrão unificado)
# ==========================================================
from utils.integration_insumos import processar_insumo
from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao

# ==========================================================
# ⚙️ Configuração inicial
# ==========================================================
st.set_page_config(
    page_title="🔧 Insumos – Upload e Integração",
    layout="wide",
    page_icon="🧩"
)

# Aplicar estilo e cabeçalho institucional
aplicar_estilo_global()
exibir_cabecalho_padrao(
    "🔧 Módulo de Insumos",
    "Envie documentos administrativos para processamento e integração automatizada "
    "com os módulos DFD, ETP, TR e Edital."
)
st.divider()

# ==========================================================
# 📂 Interface de Upload
# ==========================================================
st.subheader("📎 Envio de documento administrativo")

uploaded_file = st.file_uploader(
    "Selecione o arquivo de insumo (formatos aceitos: TXT, DOCX, PDF)",
    type=["txt", "docx", "pdf"],
    key="insumo_upload"
)

# ==========================================================
# 🧭 Seleção do módulo de destino
# ==========================================================
artefato_opcoes = ["DFD", "ETP", "TR", "EDITAL"]
artefato = st.selectbox(
    "Selecione o módulo de destino do insumo:",
    artefato_opcoes,
    key="insumo_destino"
)

# ==========================================================
# 🚀 Processamento automático (com IA institucional)
# ==========================================================
if uploaded_file is not None:
    st.success(f"📄 Arquivo detectado: {uploaded_file.name}")

    if st.button(f"🚀 Processar e encaminhar para {artefato}", key="btn_processar_insumo"):
        with st.spinner(f"Processando insumo para o módulo {artefato}..."):
            try:
                # ✅ Processamento via motor IA institucional (AIClient encapsulado)
                resultado = processar_insumo(uploaded_file, artefato)

                if resultado:
                    # Diretório de exportação institucional
                    export_dir = Path("exports") / "insumos" / "json"
                    export_dir.mkdir(parents=True, exist_ok=True)

                    # Nome final do JSON salvo
                    nome_base = Path(uploaded_file.name).stem
                    nome_json = f"{nome_base}_{artefato.lower()}.json"
                    caminho_json = export_dir / nome_json

                    # Gravar o resultado consolidado
                    with open(caminho_json, "w", encoding="utf-8") as f:
                        json.dump(resultado, f, ensure_ascii=False, indent=2)

                    st.success(f"✅ Insumo {artefato} processado com sucesso e salvo como `{nome_json}`.")
                    st.toast("💾 Resultado armazenado em exports/insumos/json/", icon="📁")
                else:
                    st.warning("⚠️ O processamento não retornou dados válidos. Verifique o arquivo enviado.")
            except Exception as e:
                st.error(f"❌ Erro ao processar insumo: {e}")
else:
    st.info("Aguardando seleção de arquivo para iniciar o processamento.")

# ==========================================================
# 🗒️ Histórico de insumos processados
# ==========================================================
st.divider()
st.subheader("📚 Histórico de insumos disponíveis")

EXPORTS_JSON_DIR = os.path.join("exports", "insumos", "json")

if os.path.exists(EXPORTS_JSON_DIR):
    arquivos = sorted(
        [f for f in os.listdir(EXPORTS_JSON_DIR) if f.endswith(".json")],
        reverse=True
    )

    if arquivos:
        for arquivo in arquivos[:5]:
            caminho = os.path.join(EXPORTS_JSON_DIR, arquivo)
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                with st.expander(f"🗂️ {arquivo}"):
                    st.json(dados)
            except Exception:
                st.warning(f"⚠️ Não foi possível ler o arquivo {arquivo}.")
    else:
        st.info("Nenhum insumo processado ainda.")
else:
    st.info("Nenhum insumo processado ainda.")

# ==========================================================
# 🌟 Rodapé institucional
# ==========================================================
st.divider()
st.caption(
    "📎 Módulo de Insumos – SynapseNext (TJSP/SAAB). "
    "Os insumos processados são automaticamente integrados aos módulos DFD, ETP, TR e Edital."
)
