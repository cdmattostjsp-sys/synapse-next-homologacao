# ==============================
# pages/06_📜 Edital – Minuta do Edital.py  –  SynapseNext / SAAB TJSP
# ==============================

import os, sys, json
from datetime import datetime
from io import BytesIO
from pathlib import Path
import streamlit as st
from docx import Document

# ==========================================================
# 🔍 Imports e configuração de ambiente
# ==========================================================

from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
from utils.integration_edital import (
    integrar_com_contexto,
    processar_insumo_edital,
    gerar_edital_docx,
    gerar_rascunho_edital,
)

st.set_page_config(page_title="📜 Edital – Minuta", layout="wide", page_icon="📜")
aplicar_estilo_global()

# ==========================================================
# 🏛️ Cabeçalho institucional
# ==========================================================
exibir_cabecalho_padrao(
    "📜 Minuta do Edital de Licitação",
    "Geração automatizada com IA institucional a partir dos artefatos DFD, ETP e TR"
)
st.divider()

# ==========================================================
# 📂 Contexto cumulativo
# ==========================================================
contexto = integrar_com_contexto(st.session_state)
if contexto:
    st.success("📎 Dados consolidados automaticamente dos módulos anteriores (DFD, ETP, TR).")
else:
    st.info("Nenhum insumo ativo detectado. Você pode gerar um edital autônomo ou enviar insumos pela página **INSUMOS**.")

# ==========================================================
# 🧠 Processamento IA institucional (caso ainda não feito)
# ==========================================================
if "edital_resultado" not in st.session_state:
    if st.button("🤖 Gerar minuta do Edital com IA institucional"):
        with st.spinner("Processando minuta com base no contexto e nos modelos do TJSP..."):
            # Gera um edital fictício vazio (sem upload, usando contexto)
            resultado = processar_insumo_edital(
                arquivo=BytesIO(b""),
                contexto_previo=contexto
            )
            st.session_state["edital_resultado"] = resultado
            st.success("✅ Minuta gerada com sucesso! Você pode revisar e exportar o documento.")
            st.rerun()

# ==========================================================
# 🧾 Exibição do resultado IA
# ==========================================================
if "edital_resultado" in st.session_state:
    resultado = st.session_state["edital_resultado"]
    campos = resultado.get("campos_ai", {})
    rascunho_texto = gerar_rascunho_edital(campos)

    st.subheader("📄 Rascunho do Edital Gerado")
    st.text_area("Pré-visualização", rascunho_texto, height=450)

    # Caminho do arquivo DOCX gerado automaticamente
    docx_path = resultado.get("docx_path")
    if docx_path and Path(docx_path).exists():
        with open(docx_path, "rb") as f:
            st.download_button(
                label="📤 Baixar Edital Oficial (DOCX)",
                data=f,
                file_name=Path(docx_path).name,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

    # Exibe informações complementares
    st.markdown("### ℹ️ Contexto Utilizado")
    st.json(resultado.get("contexto_usado", []))

    st.caption("📎 Documento gerado com base nos modelos institucionais e no contexto DFD/ETP/TR. Compatível com a Lei nº 14.133/2021.")

else:
    st.warning("A minuta ainda não foi gerada. Clique em **'🤖 Gerar minuta do Edital com IA institucional'** para iniciar o processamento.")
