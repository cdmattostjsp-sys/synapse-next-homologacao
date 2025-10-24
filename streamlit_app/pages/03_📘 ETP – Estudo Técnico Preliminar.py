# ==========================================================
# 📘 ETP – Estudo Técnico Preliminar
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# ==========================================================

import streamlit as st

st.set_page_config(
    page_title="📘 ETP – Estudo Técnico Preliminar",
    layout="wide",
    page_icon="📘",
)

# Estilo / cabeçalho institucional
from utils.ui_components import aplicar_estilo_global, exibir_cabecalho_padrao
aplicar_estilo_global()

# Export DOCX
from io import BytesIO
from docx import Document
from docx.shared import Pt
# Novos utilitários de integração e IA
from utils.integration_dfd import load_dfd_from_json
from utils.knowledge_loader import read_txt_files
from utils.agents_bridge import AgentsBridge


# ==========================================================
# 🏛️ Cabeçalho institucional
# ==========================================================
exibir_cabecalho_padrao(
    "📘 Estudo Técnico Preliminar (ETP)",
    "Pré-preenchimento automático a partir do DFD + complementação técnica"
)
st.divider()

# ==========================================================
# 📂 Leitura automática do DFD exportado
# ==========================================================
with st.expander("📂 Fonte de dados (DFD)", expanded=True):
    dfd_data = load_dfd_from_json()
    if dfd_data:
        st.success("✅ Arquivo 'exports/dfd_data.json' encontrado e carregado.")
        st.json(dfd_data)
    else:
        st.warning("⚠️ Arquivo 'exports/dfd_data.json' não encontrado. O ETP poderá ser preenchido manualmente.")


# ==========================================================
# 🔎 Utilitários: normalização de defaults
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


def _defaults_etp() -> dict:
    """
    Define valores padrão do ETP com base (1) no DFD já gerado e (2) no insumo.
    Prioridade: last_dfd > last_insumo.campos_ai > vazio.
    """
    last_dfd = st.session_state.get("last_dfd", {}) or {}
    from_insumo = _extract_from_last_insumo()

    # Campos herdáveis do DFD
    unidade = last_dfd.get("unidade_solicitante") or from_insumo.get("unidade_solicitante", "")
    responsavel_herdado = last_dfd.get("responsavel") or from_insumo.get("responsavel", "")
    objeto = last_dfd.get("objeto") or from_insumo.get("objeto", "")
    justificativa = last_dfd.get("justificativa") or from_insumo.get("justificativa", "")
    riscos = last_dfd.get("riscos") or from_insumo.get("riscos", "")

    # Campos próprios do ETP (podem vir vazios para o usuário completar)
    defaults = {
        "unidade_solicitante": unidade,
        "responsavel_tecnico": responsavel_herdado,    # pode editar para o responsável técnico formal
        "objeto": objeto,
        "justificativa": justificativa,
        "resultados_esperados": "",
        "solucoes_consideradas": "",
        "justificativa_tecnica_economica": "",
        "riscos": riscos,
        "recomendacao_final": "",
    }
    return defaults


# ==========================================================
# 🔗 Avisos de contexto
# ==========================================================
col_a, col_b = st.columns([1, 1])
with col_a:
    if "last_dfd" in st.session_state and st.session_state["last_dfd"]:
        st.success("✅ DFD detectado: o ETP será pré-preenchido com os dados do DFD.")
    else:
        st.warning("ℹ️ Nenhum DFD encontrado na sessão. Você pode preencher o ETP manualmente.")
with col_b:
    if "last_insumo" in st.session_state and st.session_state["last_insumo"]:
        insumo = st.session_state["last_insumo"]
        st.info(f"📎 Insumo ativo: {insumo.get('nome','—')} (Artefato: {insumo.get('artefato','—')})")

st.divider()


# ==========================================================
# 🧾 Formulário ETP (com auto-preenchimento)
# ==========================================================
st.subheader("1️⃣ Entrada – Informações do ETP")

defaults = _defaults_etp()

with st.form("form_etp"):
    unidade = st.text_input("Unidade solicitante", value=defaults.get("unidade_solicitante", ""))
    responsavel_tecnico = st.text_input("Responsável técnico", value=defaults.get("responsavel_tecnico", ""))
    objeto = st.text_area("Objeto da contratação", value=defaults.get("objeto", ""), height=90)
    justificativa = st.text_area("Justificativa técnica da necessidade", value=defaults.get("justificativa", ""), height=110)
    resultados = st.text_area("Resultados esperados", value=defaults.get("resultados_esperados", ""), height=100)
    solucoes = st.text_area("Soluções existentes/consideradas (alternativas, padrões, catálogos)", value=defaults.get("solucoes_consideradas", ""), height=110)
    justificativa_te = st.text_area("Justificativa técnico-econômica (custo-benefício, eficiência, vantajosidade)", value=defaults.get("justificativa_tecnica_economica", ""), height=110)
    riscos = st.text_area("Principais riscos identificados", value=defaults.get("riscos", ""), height=90)
    recomendacao = st.text_area("Recomendação técnica final", value=defaults.get("recomendacao_final", ""), height=90)

    submitted = st.form_submit_button("💾 Gerar rascunho do ETP")

# ==========================================================
# 💾 Resultado (rascunho) e persistência
# ==========================================================
if submitted:
    st.success("✅ Rascunho do ETP gerado com sucesso!")
    etp_data = {
        "unidade_solicitante": unidade,
        "responsavel_tecnico": responsavel_tecnico,
        "objeto": objeto,
        "justificativa": justificativa,
        "resultados_esperados": resultados,
        "solucoes_consideradas": solucoes,
        "justificativa_tecnica_economica": justificativa_te,
        "riscos": riscos,
        "recomendacao_final": recomendacao,
    }
    st.json(etp_data)
    st.session_state["last_etp"] = etp_data

# ==========================================================
# ⚙️ Geração assistida por IA institucional (SynapseNext)
# ==========================================================
st.divider()
st.subheader("⚙️ Geração com IA institucional")

usar_kb = st.checkbox("Enriquecer com Knowledge Base (ETP + legislação)", value=True)
max_chars_kb = st.slider("Limite de caracteres da KB", min_value=2000, max_value=40000, value=20000, step=1000)

if st.button("🤖 Gerar rascunho com IA (ETP)"):
    metadata = {
        "unidade": st.session_state.get("last_etp", {}).get("unidade_solicitante"),
        "objeto": st.session_state.get("last_etp", {}).get("objeto"),
        "justificativa": st.session_state.get("last_etp", {}).get("justificativa"),
        "riscos": st.session_state.get("last_etp", {}).get("riscos"),
        "responsavel": st.session_state.get("last_etp", {}).get("responsavel_tecnico"),
        "_fonte_dfd": dfd_data,
    }

    # (Opcional) Carregar conhecimento contextual
    kb_context = ""
    if usar_kb:
        kb_context = read_txt_files(["ETP", "legislacao"], max_chars=max_chars_kb)
        if kb_context:
            metadata["contexto_institucional"] = kb_context

    try:
        bridge = AgentsBridge("ETP")
        doc = bridge.generate(metadata)
        st.session_state["ETP_AI"] = doc
        st.success("✅ Rascunho do ETP gerado com sucesso pela IA institucional.")
        with st.expander("📄 Prévia do Rascunho (JSON)", expanded=False):
            st.json(doc)
    except Exception as e:
        st.error(f"Falha ao gerar rascunho com IA: {e}")


# ==========================================================
# 📤 Exportação do último ETP (mesmo após reload)
# ==========================================================
if "last_etp" in st.session_state and st.session_state["last_etp"]:
    st.divider()
    st.subheader("📤 Exportação de Documento")
    st.info("Você pode baixar o último ETP gerado em formato Word editável.")

    etp_data = st.session_state["last_etp"]

    # Geração do DOCX (fora do submit, persiste após reload)
    doc = Document()
    title = doc.add_heading("Estudo Técnico Preliminar (ETP)", level=1)
    for p in doc.paragraphs:
        for run in p.runs:
            run.font.size = Pt(11)

    def add_field(label, value):
        para = doc.add_paragraph()
        run1 = para.add_run(f"{label}: ")
        run1.bold = True
        para.add_run(value or "—")

    add_field("Unidade solicitante", etp_data["unidade_solicitante"])
    add_field("Responsável técnico", etp_data["responsavel_tecnico"])
    add_field("Objeto", etp_data["objeto"])
    add_field("Justificativa", etp_data["justificativa"])
    add_field("Resultados esperados", etp_data["resultados_esperados"])
    add_field("Soluções consideradas", etp_data["solucoes_consideradas"])
    add_field("Justificativa técnico-econômica", etp_data["justificativa_tecnica_economica"])
    add_field("Riscos", etp_data["riscos"])
    add_field("Recomendação técnica final", etp_data["recomendacao_final"])

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    st.download_button(
        label="💾 Baixar ETP_rascunho.docx",
        data=buffer,
        file_name="ETP_rascunho.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

# ==========================================================
# 📤 Exportação do rascunho gerado pela IA
# ==========================================================
if "ETP_AI" in st.session_state and st.session_state["ETP_AI"]:
    st.divider()
    st.subheader("📤 Exportação de Rascunho (IA)")
    doc = st.session_state["ETP_AI"]
    try:
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "exports", "ETP_rascunho.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        import json
        with open(path, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=2)
        st.success(f"Arquivo salvo: {path}")
    except Exception as e:
        st.error(f"Falha ao salvar rascunho IA: {e}")

# ==========================================================
# 🛈 Observações
# ==========================================================
st.caption(
    """
    • O ETP herda automaticamente dados do DFD quando disponível; você pode editar livremente antes de gerar o rascunho.
    • O rascunho é persistido em `st.session_state["last_etp"]` e pode ser exportado mesmo após recarregar a página.
    • Caso não exista DFD ativo, o ETP pode ser preenchido manualmente ou por inferências do insumo.
    """
)
