import sys, os
import streamlit as st
from utils.agents_bridge import AgentsBridge
from utils.integration_etp import export_etp_to_json
from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
from io import BytesIO
from docx import Document
import json

# ==========================================================
# 📘 ETP – Estudo Técnico Preliminar
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# ==========================================================
st.set_page_config(page_title="📘 ETP – Estudo Técnico Preliminar", layout="wide", page_icon="📘")
aplicar_estilo_global()

exibir_cabecalho_padrao(
    "📘 Estudo Técnico Preliminar (ETP)",
    "Pré-preenchimento automático a partir de insumos + validação IA"
)
st.divider()

# ==========================================================
# 🔍 Detecção do Insumo Ativo
# ==========================================================
insumo = st.session_state.get("last_insumo")

def _extract_defaults(insumo_obj):
    if not insumo_obj:
        return {}
    raw = insumo_obj.get("campos_ai", {}) or {}
    if isinstance(raw, dict) and "campos_ai" in raw and isinstance(raw["campos_ai"], dict):
        return raw["campos_ai"]
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str):
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict) and "campos_ai" in parsed:
                return parsed["campos_ai"]
            return parsed
        except Exception:
            return {}
    return {}

if insumo and insumo.get("artefato") in {"ETP", "TR"}:
    st.success(f"📎 Insumo ativo detectado: {insumo.get('nome', '—')} (Artefato: {insumo.get('artefato', '—')})")
    with st.expander("🧾 Prévia do insumo (texto legível)", expanded=False):
        st.text((insumo.get("conteudo", "") or "")[:1500])
    defaults = _extract_defaults(insumo)
else:
    st.info("Nenhum insumo ativo encontrado. Você pode preencher manualmente ou enviar um documento na aba **🔧 Insumos**.")
    defaults = {}

# ==========================================================
# 🎨 Ajuste visual institucional SAAB – Botões azuis
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
# 🧾 Formulário ETP
# ==========================================================
st.subheader("1️⃣ Entrada – Estudo Técnico Preliminar")

with st.form("form_etp"):
    requisitos = st.text_area("Requisitos mínimos e desempenho esperado", value=defaults.get("requisitos", ""), height=100)
    custos = st.text_area("Estimativa de custos", value=defaults.get("custos", ""), height=80)
    riscos = st.text_area("Riscos associados", value=defaults.get("riscos", ""), height=80)
    responsavel = st.text_input("Responsável técnico", value=defaults.get("responsavel_tecnico", ""))

    # 🔵 Botões no padrão institucional SAAB
    col1, col2 = st.columns(2)
    with col1:
        gerar_ia = st.form_submit_button("⚙️ Gerar rascunho com IA institucional")
    with col2:
        gerar_manual = st.form_submit_button("💾 Gerar rascunho manual")

st.caption("💡 O botão '⚙️ Gerar rascunho com IA institucional' usa o agente ETP.IA para gerar automaticamente o texto técnico.")

# ==========================================================
# 💡 Geração IA Institucional
# ==========================================================
if gerar_ia:
    st.info("Executando agente ETP institucional...")
    metadata = {
        "requisitos": requisitos,
        "custos": custos,
        "riscos": riscos,
        "responsavel_tecnico": responsavel
    }
    try:
        bridge = AgentsBridge("ETP")
        resultado = bridge.generate(metadata)
        st.success("✅ Rascunho gerado com sucesso pelo agente ETP.IA!")
        st.json(resultado)
        st.session_state["last_etp"] = resultado.get("secoes", {})
    except Exception as e:
        st.error(f"Erro ao gerar rascunho com IA: {e}")

# ==========================================================
# 💾 Resultado Manual
# ==========================================================
if gerar_manual:
    etp_data = {
        "requisitos": requisitos,
        "custos": custos,
        "riscos": riscos,
        "responsavel_tecnico": responsavel
    }
    st.success("✅ Rascunho de ETP gerado manualmente!")
    st.json(etp_data)
    st.session_state["last_etp"] = etp_data

# ==========================================================
# 📤 Exportação
# ==========================================================
if "last_etp" in st.session_state and st.session_state["last_etp"]:
    st.divider()
    st.subheader("📤 Exportação de Documento")
    st.info("Baixe o último ETP gerado em formato Word editável.")

    etp_data = st.session_state["last_etp"]
    doc = Document()
    doc.add_heading("Estudo Técnico Preliminar (ETP)", level=1)
    for k, v in etp_data.items():
        p = doc.add_paragraph()
        p.add_run(f"{k}: ").bold = True
        p.add_run(str(v) or "—")

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    st.download_button("💾 Baixar ETP_rascunho.docx", buffer, file_name="ETP_rascunho.docx")

    st.markdown("---")
    if st.button("📦 Exportar ETP (JSON)"):
        etp_payload = {
            "requisitos": etp_data.get("requisitos", ""),
            "custos": etp_data.get("custos", ""),
            "riscos": etp_data.get("riscos", ""),
            "responsavel_tecnico": etp_data.get("responsavel_tecnico", "")
        }
        try:
            path = export_etp_to_json(etp_payload)
            st.success(f"✅ ETP exportado com sucesso para {path}")
        except Exception as e:
            st.error(f"Falha ao exportar ETP: {e}")

st.caption("💡 *Dica:* O botão '⚙️ Gerar rascunho com IA institucional' usa o agente ETP.IA para gerar automaticamente o texto técnico.")
