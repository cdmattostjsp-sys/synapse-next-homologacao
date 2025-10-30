import streamlit as st
from utils.integration_dfd import export_dfd_to_json
from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
from utils.agents_bridge import AgentsBridge
from io import BytesIO
from docx import Document
from docx.shared import Pt
import json

# ==========================================================
# 📄 DFD – Documento de Formalização da Demanda
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# ==========================================================
st.set_page_config(page_title="📄 DFD – Formalização da Demanda", layout="wide", page_icon="📄")
aplicar_estilo_global()

exibir_cabecalho_padrao(
    "📄 Documento de Formalização da Demanda (DFD)",
    "Pré-preenchimento automático a partir de insumos + validação IA"
)
st.divider()

# ==========================================================
# 🔍 Detecção e normalização do Insumo Ativo
# ==========================================================
insumo = st.session_state.get("last_insumo")

def _extract_defaults(insumo_obj) -> dict:
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

if insumo and insumo.get("artefato") in {"DFD", "ETP", "TR"}:
    st.success(f"📎 Insumo ativo detectado: {insumo.get('nome','—')} (Artefato: {insumo.get('artefato','—')})")
    with st.expander("🧾 Prévia do insumo (texto legível)", expanded=False):
        st.text((insumo.get("conteudo", "") or "")[:1500])
    defaults = _extract_defaults(insumo)
else:
    st.info("Nenhum insumo ativo encontrado. Você pode preencher manualmente ou enviar um documento na aba **🔧 Insumos**.")
    defaults = {}

# ==========================================================
# 🧾 Formulário Institucional
# ==========================================================
st.subheader("1️⃣ Entrada – Formulário Institucional")

with st.form("form_dfd"):
    unidade = st.text_input("Unidade solicitante", value=defaults.get("unidade_solicitante", ""))
    responsavel = st.text_input("Responsável pela demanda", value=defaults.get("responsavel", ""))
    objeto = st.text_area("Objeto da contratação", value=defaults.get("objeto", ""), height=100)
    justificativa = st.text_area("Justificativa da necessidade", value=defaults.get("justificativa", ""), height=100)
    quantidade = st.text_area("Quantidade e escopo", value=defaults.get("quantidade", ""), height=80)
    urgencia = st.text_area("Urgência (se aplicável)", value=defaults.get("urgencia", ""), height=80)
    riscos = st.text_area("Riscos identificados", value=defaults.get("riscos", ""), height=80)
    alinhamento = st.text_area("Alinhamento estratégico", value=defaults.get("alinhamento_planejamento", ""), height=80)
    gerar_ia = st.form_submit_button("⚙️ Gerar rascunho com IA institucional")
    submitted = st.form_submit_button("�� Gerar rascunho manual")

# ==========================================================
# 💡 Geração IA Institucional
# ==========================================================
if gerar_ia:
    st.info("Executando agente DFD institucional...")
    metadata = {
        "unidade": unidade,
        "descricao": objeto,
        "justificativa": justificativa,
        "quantidade": quantidade,
        "riscos": riscos,
        "responsavel": responsavel,
        "alinhamento": alinhamento,
    }
    try:
        bridge = AgentsBridge("DFD")
        resultado = bridge.generate(metadata)
        st.success("✅ Rascunho gerado com sucesso pelo agente institucional DFD.IA!")
        st.json(resultado)
        st.session_state["last_dfd"] = resultado.get("secoes", {})
    except Exception as e:
        st.error(f"Erro ao gerar rascunho com IA: {e}")

# ==========================================================
# 💾 Resultado Manual
# ==========================================================
if submitted:
    dfd_data = {
        "unidade_solicitante": unidade,
        "responsavel": responsavel,
        "objeto": objeto,
        "justificativa": justificativa,
        "quantidade": quantidade,
        "urgencia": urgencia,
        "riscos": riscos,
        "alinhamento_planejamento": alinhamento,
    }
    st.success("✅ Rascunho de DFD gerado manualmente!")
    st.json(dfd_data)
    st.session_state["last_dfd"] = dfd_data

# ==========================================================
# 📤 Exportação
# ==========================================================
if "last_dfd" in st.session_state and st.session_state["last_dfd"]:
    st.divider()
    st.subheader("📤 Exportação de Documento")
    st.info("Baixe o último DFD gerado em formato Word editável.")

    dfd_data = st.session_state["last_dfd"]
    doc = Document()
    doc.add_heading("Documento de Formalização da Demanda (DFD)", level=1)
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
        dfd_payload = {
            "unidade": dfd_data.get("unidade_solicitante", ""),
            "descricao": dfd_data.get("objeto", ""),
            "motivacao": dfd_data.get("justificativa", ""),
            "quantidade": dfd_data.get("quantidade", ""),
            "responsavel": dfd_data.get("responsavel", ""),
            "riscos": dfd_data.get("riscos", ""),
            "alinhamento": dfd_data.get("alinhamento_planejamento", "")
        }
        try:
            path = export_dfd_to_json(dfd_payload)
            st.success(f"✅ DFD exportado com sucesso para {path}")
        except Exception as e:
            st.error(f"Falha ao exportar DFD: {e}")

st.caption("💡 *Dica:* O botão '⚙️ Gerar rascunho com IA institucional' usa o agente DFD.IA com base nos metadados preenchidos.")

