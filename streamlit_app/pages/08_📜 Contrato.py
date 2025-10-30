# ==========================================================
# 📜 SynapseNext vNext – Contrato Administrativo
# Secretaria de Administração e Abastecimento (SAAB/TJSP)
# ==========================================================

import streamlit as st
from datetime import datetime
from io import BytesIO
from docx import Document
import json, os

# ==========================================================
# 🔧 Imports institucionais
# ==========================================================
from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
from utils.agents_bridge import AgentsBridge
from utils.formatter_docx import markdown_to_docx
from utils.next_pipeline import registrar_log

# ==========================================================
# ⚙️ Configuração de página
# ==========================================================
st.set_page_config(
    page_title="📜 Contrato Administrativo",
    layout="wide",
    page_icon="📜"
)
aplicar_estilo_global()

exibir_cabecalho_padrao(
    "📜 Contrato Administrativo",
    "Formalização contratual automatizada com base no Termo de Referência (TR)"
)
st.divider()

# ==========================================================
# 🧩 Recupera TR ativo (vNext)
# ==========================================================
if st.session_state.get("last_tr"):
    tr_data = st.session_state["last_tr"]
    st.success("📎 Termo de Referência detectado – dados importados automaticamente.")
else:
    st.info("Nenhum TR ativo encontrado. Preencha manualmente ou gere via IA.")
    tr_data = {}

# ==========================================================
# 🧾 Formulário Institucional do Contrato
# ==========================================================
st.subheader("1️⃣ Entrada – Dados Contratuais")

with st.form("form_contrato"):
    col1, col2 = st.columns(2)
    with col1:
        objeto = st.text_area("Objeto do contrato", value=tr_data.get("objeto", ""), height=80)
        partes = st.text_area("Partes contratantes", placeholder="Ex.: TJSP e a empresa XYZ Ltda.", height=70)
        valor_global = st.text_input("Valor global (R$)", value=tr_data.get("estimativa_valor", ""))
        prazo_execucao = st.text_input("Prazo de execução", value=tr_data.get("prazo_execucao", ""))
        vigencia = st.text_input("Vigência contratual", placeholder="Ex.: 12 meses contados da assinatura.")
    with col2:
        obrigacoes_contratada = st.text_area("Obrigações da contratada", height=90)
        obrigacoes_contratante = st.text_area("Obrigações da contratante", height=90)
        garantias = st.text_area("Garantias e penalidades", height=80)
        fiscalizacao = st.text_area("Fiscalização e acompanhamento", height=70)
        assinatura = st.text_area("Assinaturas / Representantes", height=70)

    gerar_ia = st.form_submit_button("⚙️ Gerar rascunho com IA institucional")
    gerar_manual = st.form_submit_button("💾 Gerar rascunho manual")

# ==========================================================
# ⚙️ Geração via IA Institucional (Contrato.IA)
# ==========================================================
if gerar_ia:
    st.info("Executando agente Contrato institucional...")
    metadata = {
        "objeto": objeto,
        "valor_global": valor_global,
        "prazo_execucao": prazo_execucao,
        "vigencia": vigencia,
        "garantias": garantias,
        "fiscalizacao": fiscalizacao,
    }
    try:
        bridge = AgentsBridge("CONTRATO")
        resultado = bridge.generate(metadata)
        st.success("✅ Rascunho gerado com sucesso pelo agente Contrato.IA!")
        st.json(resultado)
        st.session_state["last_contrato"] = resultado.get("secoes", {})
        registrar_log("CONTRATO", "gerar_rascunho_ia")
    except Exception as e:
        st.error(f"Erro ao gerar rascunho com IA: {e}")

# ==========================================================
# 💾 Geração Manual (formulário)
# ==========================================================
if gerar_manual:
    contrato_data = {
        "objeto": objeto,
        "partes": partes,
        "valor_global": valor_global,
        "prazo_execucao": prazo_execucao,
        "vigencia": vigencia,
        "obrigacoes_contratada": obrigacoes_contratada,
        "obrigacoes_contratante": obrigacoes_contratante,
        "garantias": garantias,
        "fiscalizacao": fiscalizacao,
        "assinatura": assinatura,
    }
    st.success("✅ Rascunho de contrato gerado manualmente!")
    st.json(contrato_data)
    st.session_state["last_contrato"] = contrato_data
    registrar_log("CONTRATO", "gerar_rascunho_manual")

# ==========================================================
# 📤 Exportação de Contrato
# ==========================================================
if st.session_state.get("last_contrato"):
    st.divider()
    st.subheader("📤 Exportação de Documento")

    contrato_data = st.session_state["last_contrato"]
    doc = Document()
    doc.add_heading("Contrato Administrativo", level=1)
    for k, v in contrato_data.items():
        p = doc.add_paragraph()
        p.add_run(f"{k}: ").bold = True
        p.add_run(str(v) or "—")

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    st.download_button("💾 Baixar Contrato_rascunho.docx", buffer, file_name="Contrato_rascunho.docx")

    if st.button("📦 Exportar Contrato (JSON)"):
        os.makedirs("exports", exist_ok=True)
        path = "exports/contrato_teste.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(contrato_data, f, ensure_ascii=False, indent=2)
        st.success(f"✅ Contrato exportado com sucesso para {path}")
        registrar_log("CONTRATO", "exportar_json")

st.caption("💡 O agente Contrato.IA gera automaticamente a minuta contratual com base no TR ativo e nos dados informados.")
