# ==========================================================
# pages/02_📄 DFD – Formalização da Demanda.py
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# ==========================================================

import os
import json
import streamlit as st
from pathlib import Path
from io import BytesIO
from docx import Document

# ==========================================================
# 📦 Imports institucionais
# ==========================================================
from utils.agents_bridge import AgentsBridge
from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao

# ==========================================================
# ⚙️ Configuração inicial
# ==========================================================
st.set_page_config(page_title="📄 DFD – Formalização da Demanda", layout="wide", page_icon="📄")
aplicar_estilo_global()

exibir_cabecalho_padrao(
    "📄 Formalização da Demanda (DFD)",
    "Registro institucional da demanda e geração de rascunho com IA"
)
st.divider()

# ==========================================================
# 🧾 Formulário DFD
# ==========================================================
st.subheader("1️⃣ Entrada – Formalização da Demanda")

with st.form("form_dfd"):
    col1, col2 = st.columns(2)
    with col1:
        unidade = st.text_input("Unidade Demandante", placeholder="Ex.: Secretaria de Administração e Abastecimento – SAAB")
        responsavel = st.text_input("Responsável pela Demanda")
        prazo = st.text_input("Prazo Estimado para Atendimento")
    with col2:
        descricao = st.text_area("Descrição da Necessidade", height=100)
        motivacao = st.text_area("Motivação da Contratação", height=100)
        estimativa_valor = st.number_input("Estimativa de Valor (R$)", min_value=0.0, step=1000.0)

    colb1, colb2 = st.columns(2)
    with colb1:
        gerar_ia = st.form_submit_button("⚙️ Gerar rascunho com IA institucional")
    with colb2:
        salvar_manual = st.form_submit_button("💾 Salvar dados manualmente")

# ==========================================================
# 🎨 Estilo institucional SAAB – botões
# ==========================================================
st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #003366 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    height: 2.8em !important;
    font-weight: 500 !important;
}
div.stButton > button:first-child:hover {
    background-color: #002244 !important;
    color: white !important;
    transition: 0.2s;
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# 🤖 Geração IA Institucional
# ==========================================================
if gerar_ia:
    st.info("Executando agente DFD institucional...")
    metadata = {
        "unidade": unidade,
        "responsavel": responsavel,
        "prazo": prazo,
        "descricao": descricao,
        "motivacao": motivacao,
        "estimativa_valor": estimativa_valor,
    }
    try:
        bridge = AgentsBridge("DFD")
        resultado = bridge.generate(metadata)
        st.success("✅ Rascunho gerado com sucesso pelo agente DFD.IA!")
        st.json(resultado)
        st.session_state["last_dfd"] = resultado.get("secoes", {})

        # salva JSON institucional
        exports_dir = Path("exports")
        exports_dir.mkdir(exist_ok=True)
        json_path = exports_dir / "dfd_data.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)
        st.info(f"💾 Arquivo exportado: {json_path}")

    except Exception as e:
        st.error(f"Erro ao gerar rascunho com IA: {e}")

# ==========================================================
# 💾 Salvamento manual (fallback)
# ==========================================================
if salvar_manual:
    dfd_data = {
        "unidade": unidade,
        "responsavel": responsavel,
        "prazo": prazo,
        "descricao": descricao,
        "motivacao": motivacao,
        "estimativa_valor": estimativa_valor
    }
    st.success("✅ Dados do DFD salvos manualmente.")
    st.json(dfd_data)
    st.session_state["last_dfd"] = dfd_data

# ==========================================================
# 📤 Exportação do Documento
# ==========================================================
if "last_dfd" in st.session_state and st.session_state["last_dfd"]:
    st.divider()
    st.subheader("📤 Exportação de Documento")
    st.info("Baixe o último DFD gerado em formato Word editável.")

    dfd_data = st.session_state["last_dfd"]
    doc = Document()
    doc.add_heading("Formalização da Demanda (DFD)", level=1)
    for k, v in dfd_data.items():
        p = doc.add_paragraph()
        p.add_run(f"{k}: ").bold = True
        p.add_run(str(v) or "—")

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    st.download_button("💾 Baixar DFD_rascunho.docx", buffer, file_name="DFD_rascunho.docx")

    st.markdown("---")
    if st.button("📦 Exportar DFD (JSON)"):
        try:
            exports_dir = Path("exports")
            exports_dir.mkdir(exist_ok=True)
            json_path = exports_dir / "dfd_data.json"
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(dfd_data, f, ensure_ascii=False, indent=2)
            st.success(f"✅ DFD exportado com sucesso para {json_path}")
        except Exception as e:
            st.error(f"Falha ao exportar DFD: {e}")

st.caption("💡 *Dica:* O botão '⚙️ Gerar rascunho com IA institucional' usa o agente DFD.IA para gerar automaticamente o texto técnico.")
