# ==========================================================
# 📑 TR – Termo de Referência
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# ==========================================================

import streamlit as st

st.set_page_config(
    page_title="📑 TR – Termo de Referência",
    layout="wide",
    page_icon="📑",
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
    "📑 Termo de Referência (TR)",
    "Pré-preenchimento a partir do ETP/DFD + complementação dos requisitos e condições"
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


def _defaults_tr() -> dict:
    """
    Define valores padrão do TR com base (1) no ETP já gerado, (2) no DFD e (3) no insumo.
    Prioridade: last_etp > last_dfd > last_insumo.campos_ai > vazio.
    """
    last_etp = st.session_state.get("last_etp", {}) or {}
    last_dfd = st.session_state.get("last_dfd", {}) or {}
    from_insumo = _extract_from_last_insumo()

    def pick(*keys, default=""):
        """Escolhe o primeiro valor não vazio na ordem de prioridade."""
        for k in keys:
            v = (
                last_etp.get(k)
                or last_dfd.get(k)
                or from_insumo.get(k)
            )
            if v:
                return v
        return default

    defaults = {
        "unidade_solicitante": pick("unidade_solicitante"),
        "responsavel_tecnico": pick("responsavel_tecnico", "responsavel"),
        "objeto": pick("objeto"),
        # Campos próprios do TR:
        "especificacao_tecnica": "",
        "quantidade": pick("quantidade"),
        "estimativa_valor": "",
        "fonte_recurso": "",
        "prazo_execucao": "",
        "criterios_julgamento": "",
        "riscos": pick("riscos"),
        "justificativa_tecnica": pick("justificativa", "justificativa_tecnica_economica"),
        "observacoes_finais": "",
    }
    return defaults


# ==========================================================
# 🔗 Avisos de contexto
# ==========================================================
col_a, col_b, col_c = st.columns([1, 1, 1])
with col_a:
    if st.session_state.get("last_etp"):
        st.success("✅ ETP detectado: o TR será pré-preenchido com base no ETP.")
    else:
        st.info("ℹ️ Nenhum ETP detectado na sessão.")

with col_b:
    if st.session_state.get("last_dfd"):
        st.success("✅ DFD detectado: dados poderão complementar o TR.")
    else:
        st.info("ℹ️ Nenhum DFD detectado na sessão.")

with col_c:
    if st.session_state.get("last_insumo"):
        insumo = st.session_state["last_insumo"]
        st.info(f"📎 Insumo ativo: {insumo.get('nome','—')} (Artefato: {insumo.get('artefato','—')})")

st.divider()


# ==========================================================
# 🧾 Formulário TR (auto-preenchido, campos editáveis)
# ==========================================================
st.subheader("1️⃣ Entrada – Informações do TR")

defaults = _defaults_tr()

with st.form("form_tr"):
    unidade = st.text_input("Unidade solicitante", value=defaults.get("unidade_solicitante", ""))
    responsavel_tecnico = st.text_input("Responsável técnico", value=defaults.get("responsavel_tecnico", ""))
    objeto = st.text_area("Objeto da contratação", value=defaults.get("objeto", ""), height=90)

    st.markdown("**Especificação técnica detalhada**")
    especificacao_tecnica = st.text_area(
        "Descreva requisitos, padrões, normas, compatibilidades, níveis de serviço (SLA), garantias etc.",
        value=defaults.get("especificacao_tecnica", ""),
        height=140
    )

    col1, col2 = st.columns(2)
    with col1:
        quantidade = st.text_input("Quantidade / Unidades de medida", value=defaults.get("quantidade", ""))
        prazo_execucao = st.text_input("Prazo de entrega / execução", value=defaults.get("prazo_execucao", ""))
    with col2:
        estimativa_valor = st.text_input("Estimativa de valor (R$)", value=defaults.get("estimativa_valor", ""))
        fonte_recurso = st.text_input("Fonte de recurso", value=defaults.get("fonte_recurso", ""))

    criterios_julgamento = st.text_area(
        "Critérios de julgamento (menor preço, técnica e preço, melhor técnica, etc.)",
        value=defaults.get("criterios_julgamento", ""),
        height=110
    )
    riscos = st.text_area("Principais riscos identificados", value=defaults.get("riscos", ""), height=100)
    justificativa_tecnica = st.text_area(
        "Justificativa técnica (vantajosidade, custo-benefício, aderência às necessidades)",
        value=defaults.get("justificativa_tecnica", ""),
        height=110
    )
    observacoes_finais = st.text_area("Observações finais", value=defaults.get("observacoes_finais", ""), height=80)

    submitted = st.form_submit_button("💾 Gerar rascunho do TR")


# ==========================================================
# 💾 Resultado (rascunho) e persistência
# ==========================================================
if submitted:
    st.success("✅ Rascunho do TR gerado com sucesso!")
    tr_data = {
        "unidade_solicitante": unidade,
        "responsavel_tecnico": responsavel_tecnico,
        "objeto": objeto,
        "especificacao_tecnica": especificacao_tecnica,
        "quantidade": quantidade,
        "estimativa_valor": estimativa_valor,
        "fonte_recurso": fonte_recurso,
        "prazo_execucao": prazo_execucao,
        "criterios_julgamento": criterios_julgamento,
        "riscos": riscos,
        "justificativa_tecnica": justificativa_tecnica,
        "observacoes_finais": observacoes_finais,
    }
    st.json(tr_data)
    st.session_state["last_tr"] = tr_data


# ==========================================================
# 📤 Exportação do último TR (mesmo após reload)
# ==========================================================
if st.session_state.get("last_tr"):
    st.divider()
    st.subheader("📤 Exportação de Documento")
    st.info("Você pode baixar o último TR gerado em formato Word editável.")

    tr_data = st.session_state["last_tr"]

    # Geração do DOCX (fora do submit, persiste após reload)
    doc = Document()
    title = doc.add_heading("Termo de Referência (TR)", level=1)
    for p in doc.paragraphs:
        for run in p.runs:
            run.font.size = Pt(11)

    def add_field(label, value):
        para = doc.add_paragraph()
        run1 = para.add_run(f"{label}: ")
        run1.bold = True
        para.add_run(value or "—")

    add_field("Unidade solicitante", tr_data["unidade_solicitante"])
    add_field("Responsável técnico", tr_data["responsavel_tecnico"])
    add_field("Objeto", tr_data["objeto"])
    doc.add_paragraph("")  # espaçamento
    doc.add_heading("Especificação técnica", level=2)
    doc.add_paragraph(tr_data["especificacao_tecnica"] or "—")

    colA = [
        ("Quantidade / Unidades de medida", tr_data["quantidade"]),
        ("Estimativa de valor (R$)", tr_data["estimativa_valor"]),
        ("Fonte de recurso", tr_data["fonte_recurso"]),
        ("Prazo de entrega / execução", tr_data["prazo_execucao"]),
    ]
    for label, value in colA:
        add_field(label, value)

    doc.add_paragraph("")  # espaçamento
    add_field("Critérios de julgamento", tr_data["criterios_julgamento"])
    add_field("Riscos identificados", tr_data["riscos"])
    add_field("Justificativa técnica", tr_data["justificativa_tecnica"])
    add_field("Observações finais", tr_data["observacoes_finais"])

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    st.download_button(
        label="💾 Baixar TR_rascunho.docx",
        data=buffer,
        file_name="TR_rascunho.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


# ==========================================================
# 🛈 Observações
# ==========================================================
st.caption(
    """
    • O TR é pré-preenchido com prioridade: ETP → DFD → Insumo (IA).
    • O rascunho é persistido em `st.session_state["last_tr"]` e pode ser exportado mesmo após recarregar a página.
    • Os campos são totalmente editáveis antes de gerar o rascunho/Word.
    """
)
