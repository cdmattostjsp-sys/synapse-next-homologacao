# ==========================================================
# 🧾 Edital – Minuta do Edital de Licitação
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# ==========================================================

import streamlit as st

st.set_page_config(
    page_title="🧾 Edital – Minuta",
    layout="wide",
    page_icon="🧾",
)

# Estilo / cabeçalho institucional
from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
aplicar_estilo_global()

# Export DOCX
from io import BytesIO
from docx import Document
from docx.shared import Pt


# ==========================================================
# 🏛️ Cabeçalho institucional
# ==========================================================
exibir_cabecalho_padrao(
    "🧾 Edital – Minuta do Edital de Licitação",
    "Pré-preenchimento a partir do TR/ETP/DFD + complementação jurídico-administrativa"
)
st.divider()


# ==========================================================
# 🔎 Utilitários: normalização de defaults (fallbacks)
# ==========================================================
def _extract_from_last_insumo() -> dict:
    """
    Fallback: extrai campos de last_insumo.campos_ai (se existir),
    aceitando dict puro, dict embrulhado ou string JSON.
    """
    import json
    insumo = st.session_state.get("last_insumo")
    if not insumo:
        return {}

    raw = insumo.get("campos_ai", {}) or {}
    if isinstance(raw, dict) and "campos_ai" in raw and isinstance(raw["campos_ai"], dict):
        return raw["campos_ai"]
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str):
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict) and "campos_ai" in parsed and isinstance(parsed["campos_ai"], dict):
                return parsed["campos_ai"]
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            return {}
    return {}


def _defaults_edital() -> dict:
    """
    Define valores padrão do Edital com base (1) no TR, (2) no ETP, (3) no DFD e (4) no insumo.
    Prioridade: last_tr > last_etp > last_dfd > last_insumo.campos_ai > vazio.
    """
    last_tr = st.session_state.get("last_tr", {}) or {}
    last_etp = st.session_state.get("last_etp", {}) or {}
    last_dfd = st.session_state.get("last_dfd", {}) or {}
    from_insumo = _extract_from_last_insumo()

    def pick(key, default=""):
        """Escolhe o primeiro valor não vazio na ordem de prioridade."""
        return (
            last_tr.get(key)
            or last_etp.get(key)
            or last_dfd.get(key)
            or from_insumo.get(key)
            or default
        )

    defaults = {
        # Identificação
        "unidade_solicitante": pick("unidade_solicitante"),
        "responsavel_tecnico": pick("responsavel_tecnico", pick("responsavel")),
        "objeto": pick("objeto"),

        # Campos jurídico-administrativos do Edital
        "modalidade": "",
        "regime_execucao": "",
        "base_legal": "Lei nº 14.133/2021",
        "justificativa_modalidade": pick("justificativa", pick("justificativa_tecnica")),

        "habilitacao": "",
        "criterios_julgamento": pick("criterios_julgamento"),
        "prazo_execucao": pick("prazo_execucao"),
        "forma_pagamento": "",
        "penalidades": "",

        "observacoes_finais": "",
    }
    return defaults


# ==========================================================
# 🔗 Avisos de contexto
# ==========================================================
col_a, col_b, col_c = st.columns([1, 1, 1])
with col_a:
    if st.session_state.get("last_tr"):
        st.success("✅ TR detectado: o Edital será pré-preenchido com base no TR.")
    else:
        st.info("ℹ️ Nenhum TR detectado na sessão.")

with col_b:
    if st.session_state.get("last_etp"):
        st.success("✅ ETP detectado: dados complementarão o Edital.")
    else:
        st.info("ℹ️ Nenhum ETP detectado na sessão.")

with col_c:
    if st.session_state.get("last_dfd"):
        st.success("✅ DFD detectado: dados de origem disponíveis.")
    else:
        st.info("ℹ️ Nenhum DFD detectado na sessão.")

if st.session_state.get("last_insumo"):
    insumo = st.session_state["last_insumo"]
    st.info(f"📎 Insumo ativo: {insumo.get('nome','—')} (Artefato: {insumo.get('artefato','—')})")

st.divider()


# ==========================================================
# 🧾 Formulário do Edital (auto-preenchido e editável)
# ==========================================================
st.subheader("1️⃣ Entrada – Informações do Edital")

defaults = _defaults_edital()

with st.form("form_edital"):
    unidade = st.text_input("Unidade solicitante", value=defaults.get("unidade_solicitante", ""))
    responsavel_tecnico = st.text_input("Responsável técnico", value=defaults.get("responsavel_tecnico", ""))
    objeto = st.text_area("Objeto da licitação", value=defaults.get("objeto", ""), height=90)

    col1, col2 = st.columns(2)
    with col1:
        modalidade = st.text_input("Modalidade de licitação", value=defaults.get("modalidade", ""))
        regime_execucao = st.text_input("Regime de execução", value=defaults.get("regime_execucao", ""))
        base_legal = st.text_input("Base legal", value=defaults.get("base_legal", "Lei nº 14.133/2021"))
    with col2:
        justificativa_modalidade = st.text_area(
            "Justificativa da escolha da modalidade / fundamentação",
            value=defaults.get("justificativa_modalidade", ""),
            height=110
        )

    st.markdown("**Condições de participação e julgamento**")
    habilitacao = st.text_area(
        "Requisitos de habilitação",
        value=defaults.get("habilitacao", ""),
        height=110
    )
    criterios_julgamento = st.text_area(
        "Critérios de julgamento",
        value=defaults.get("criterios_julgamento", ""),
        height=110
    )

    col3, col4 = st.columns(2)
    with col3:
        prazo_execucao = st.text_input("Prazo de entrega / execução", value=defaults.get("prazo_execucao", ""))
        forma_pagamento = st.text_input("Forma de pagamento", value=defaults.get("forma_pagamento", ""))
    with col4:
        penalidades = st.text_area("Penalidades e sanções", value=defaults.get("penalidades", ""), height=110)

    observacoes_finais = st.text_area("Observações finais", value=defaults.get("observacoes_finais", ""), height=80)

    submitted = st.form_submit_button("💾 Gerar rascunho do Edital")


# ==========================================================
# 💾 Resultado (rascunho) e persistência
# ==========================================================
if submitted:
    st.success("✅ Rascunho do Edital gerado com sucesso!")
    edital_data = {
        "unidade_solicitante": unidade,
        "responsavel_tecnico": responsavel_tecnico,
        "objeto": objeto,
        "modalidade": modalidade,
        "regime_execucao": regime_execucao,
        "base_legal": base_legal,
        "justificativa_modalidade": justificativa_modalidade,
        "habilitacao": habilitacao,
        "criterios_julgamento": criterios_julgamento,
        "prazo_execucao": prazo_execucao,
        "forma_pagamento": forma_pagamento,
        "penalidades": penalidades,
        "observacoes_finais": observacoes_finais,
    }
    st.json(edital_data)
    st.session_state["last_edital"] = edital_data


# ==========================================================
# 📤 Exportação do último Edital (mesmo após reload)
# ==========================================================
if st.session_state.get("last_edital"):
    st.divider()
    st.subheader("📤 Exportação de Documento")
    st.info("Você pode baixar o último Edital gerado em formato Word editável.")

    edital_data = st.session_state["last_edital"]

    # Geração do DOCX (fora do submit, persiste após reload)
    doc = Document()
    title = doc.add_heading("Minuta do Edital de Licitação", level=1)
    for p in doc.paragraphs:
        for run in p.runs:
            run.font.size = Pt(11)

    def add_field(label, value):
        para = doc.add_paragraph()
        run1 = para.add_run(f"{label}: ")
        run1.bold = True
        para.add_run(value or "—")

    # Identificação
    add_field("Unidade solicitante", edital_data["unidade_solicitante"])
    add_field("Responsável técnico", edital_data["responsavel_tecnico"])
    add_field("Objeto", edital_data["objeto"])

    # Fundamentação e modalidade
    doc.add_paragraph("")
    doc.add_heading("Modalidade, Regime e Fundamentação", level=2)
    add_field("Modalidade de licitação", edital_data["modalidade"])
    add_field("Regime de execução", edital_data["regime_execucao"])
    add_field("Base legal", edital_data["base_legal"])
    add_field("Justificativa da modalidade", edital_data["justificativa_modalidade"])

    # Condições de participação
    doc.add_paragraph("")
    doc.add_heading("Condições de Participação e Habilitação", level=2)
    doc.add_paragraph(edital_data["habilitacao"] or "—")

    # Critérios de julgamento
    doc.add_paragraph("")
    doc.add_heading("Critérios de Julgamento", level=2)
    doc.add_paragraph(edital_data["criterios_julgamento"] or "—")

    # Execução, prazos, pagamentos
    doc.add_paragraph("")
    doc.add_heading("Execução, Prazos e Pagamentos", level=2)
    add_field("Prazo de entrega / execução", edital_data["prazo_execucao"])
    add_field("Forma de pagamento", edital_data["forma_pagamento"])

    # Penalidades
    doc.add_paragraph("")
    doc.add_heading("Penalidades e Sanções", level=2)
    doc.add_paragraph(edital_data["penalidades"] or "—")

    # Observações finais
    doc.add_paragraph("")
    add_field("Observações finais", edital_data["observacoes_finais"])

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    st.download_button(
        label="💾 Baixar Edital_rascunho.docx",
        data=buffer,
        file_name="Edital_rascunho.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


# ==========================================================
# 🛈 Observações
# ==========================================================
st.caption(
    """
    • O Edital é pré-preenchido com prioridade: TR → ETP → DFD → Insumo (IA).
    • O rascunho é persistido em `st.session_state["last_edital"]` e pode ser exportado mesmo após recarregar a página.
    • Todos os campos são editáveis antes da geração do rascunho/Word.
    """
)
