import streamlit as st
from utils.integration_dfd import export_dfd_to_json

# ==========================================================
# 📄 DFD – Documento de Formalização da Demanda
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# ==========================================================

st.set_page_config(page_title="📄 DFD – Formalização da Demanda", layout="wide", page_icon="📄")

from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
aplicar_estilo_global()

# Export DOCX
from io import BytesIO
from docx import Document
from docx.shared import Pt

# ==========================================================
# 🏛️ Cabeçalho institucional padronizado
# ==========================================================
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
    """
    Normaliza o dicionário 'defaults' a partir de last_insumo.campos_ai,
    aceitando os seguintes formatos:
      - dict com as chaves finais (OK)
      - dict embrulhado: {"campos_ai": {...}}
      - string JSON (tenta json.loads)
      - qualquer outro: retorna {}
    """
    import json
    if not insumo_obj:
        return {}

    raw = insumo_obj.get("campos_ai", {}) or {}

    # Caso venha embrulhado: {"campos_ai": {...}}
    if isinstance(raw, dict) and "campos_ai" in raw and isinstance(raw["campos_ai"], dict):
        return raw["campos_ai"]

    # Caso já seja um dict final
    if isinstance(raw, dict):
        return raw

    # Caso venha como string (JSON)
    if isinstance(raw, str):
        try:
            parsed = json.loads(raw)
            # pode vir embrulhado de novo
            if isinstance(parsed, dict) and "campos_ai" in parsed and isinstance(parsed["campos_ai"], dict):
                return parsed["campos_ai"]
            if isinstance(parsed, dict):
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
# 🧾 Formulário Institucional (com ou sem preenchimento IA)
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

    submitted = st.form_submit_button("💾 Gerar rascunho do DFD")

# ==========================================================
# 💾 Resultado e Exportação
# ==========================================================
if submitted:
    st.success("✅ Rascunho de DFD gerado com sucesso!")
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

    st.json(dfd_data)
    st.session_state["last_dfd"] = dfd_data

# ==========================================================
# 📤 Exportação do último DFD (mesmo após reload)
# ==========================================================
if "last_dfd" in st.session_state and st.session_state["last_dfd"]:
    st.divider()
    st.subheader("📤 Exportação de Documento")
    st.info("Você pode baixar o último DFD gerado em formato Word editável.")

    dfd_data = st.session_state["last_dfd"]

    # Geração do arquivo DOCX
    from io import BytesIO
    from docx import Document
    from docx.shared import Pt

    doc = Document()
    title = doc.add_heading("Documento de Formalização da Demanda (DFD)", level=1)
    for p in doc.paragraphs:
        for run in p.runs:
            run.font.size = Pt(11)

    def add_field(label, value):
        para = doc.add_paragraph()
        run1 = para.add_run(f"{label}: ")
        run1.bold = True
        run2 = para.add_run(value or "—")

    add_field("Unidade solicitante", dfd_data["unidade_solicitante"])
    add_field("Responsável", dfd_data["responsavel"])
    add_field("Objeto", dfd_data["objeto"])
    add_field("Justificativa", dfd_data["justificativa"])
    add_field("Quantidade / Escopo", dfd_data["quantidade"])
    add_field("Urgência", dfd_data["urgencia"])
    add_field("Riscos", dfd_data["riscos"])
    add_field("Alinhamento estratégico", dfd_data["alinhamento_planejamento"])

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    st.download_button(
        label="💾 Baixar DFD_rascunho.docx",
        data=buffer,
        file_name="DFD_rascunho.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    # ==========================================================
    # 📦 Exportação do DFD em JSON (para integração com ETP)
    # ==========================================================
    st.markdown("---")
    st.subheader("📦 Exportação para ETP (JSON)")
    st.info("Gera o arquivo 'exports/dfd_data.json', que será utilizado automaticamente pelo módulo ETP.")

    if st.button("📦 Exportar DFD (JSON)"):
        dfd_payload = {
            "unidade": dfd_data.get("unidade_solicitante", ""),
            "descricao": dfd_data.get("objeto", ""),
            "motivacao": dfd_data.get("justificativa", ""),
            "quantidade": dfd_data.get("quantidade", ""),
            "prazo": "",  # opcional – ainda não presente no DFD
            "estimativa_valor": "",  # opcional – preenchido no ETP
            "responsavel": dfd_data.get("responsavel", ""),
            "riscos": dfd_data.get("riscos", ""),
            "alinhamento": dfd_data.get("alinhamento_planejamento", "")
        }
        try:
            path = export_dfd_to_json(dfd_payload)
            st.success(f"✅ DFD exportado com sucesso para {path}")
        except Exception as e:
            st.error(f"Falha ao exportar DFD: {e}")


# ==========================================================
# 📊 Observações Técnicas
# ==========================================================
st.caption(
    """
    💡 *Dica:* Quando um insumo for processado na aba **Insumos**, o DFD será automaticamente pré-preenchido.
    O campo `st.session_state["last_insumo"]` transfere as inferências da IA entre páginas.
    """
)
