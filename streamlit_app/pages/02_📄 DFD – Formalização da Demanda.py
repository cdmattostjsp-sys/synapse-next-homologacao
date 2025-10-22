import streamlit as st

# ==========================================================
# 📄 DFD – Documento de Formalização da Demanda
# SynapseNext – Secretaria de Administração e Abastecimento (TJSP)
# ==========================================================

st.set_page_config(page_title="📄 DFD – Formalização da Demanda", layout="wide")

# ==========================================================
# 🏛️ Cabeçalho
# ==========================================================
st.markdown(
    """
    <div style='padding: 1.2rem 0; text-align: center;'>
        <h1 style='color:#800000; margin-bottom:0.3rem;'>📄 Documento de Formalização da Demanda (DFD)</h1>
        <p style='font-size:1.05rem; color:#444;'>Pré-preenchimento automático a partir de insumos + validação IA</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# 🔍 Detecção de Insumo Ativo
# ==========================================================
insumo = st.session_state.get("last_insumo")

if insumo and insumo.get("artefato") in {"DFD", "ETP", "TR"}:
    st.success(f"📎 Insumo ativo detectado: {insumo['nome']} (Artefato: {insumo['artefato']})")
    with st.expander("🧾 Prévia do insumo (texto legível)", expanded=False):
        st.text(insumo.get("conteudo", "")[:1500])
    defaults = insumo.get("campos_ai", {}) or {}
else:
    st.info("Nenhum insumo ativo encontrado. Você pode preencher manualmente ou enviar um documento na aba **🔧 Insumos**.")
    defaults = {}

# ==========================================================
# 🧾 Formulário Institucional (com ou sem preenchimento IA)
# ==========================================================
st.divider()
st.subheader("1️⃣ Entrada – Formulário Institucional")

with st.form("form_dfd"):
    unidade = st.text_input("Unidade solicitante", value=defaults.get("unidade", ""))
    responsavel = st.text_input("Responsável pela demanda", value=defaults.get("responsavel", ""))
    objeto = st.text_area("Objeto da contratação", value=defaults.get("objeto", ""), height=100)
    justificativa = st.text_area("Justificativa da necessidade", value=defaults.get("justificativa", ""), height=100)
    quantidade = st.text_area("Quantidade e escopo", value=defaults.get("quantidade", ""), height=80)
    urgencia = st.text_area("Urgência (se aplicável)", value=defaults.get("urgencia", ""), height=80)
    riscos = st.text_area("Riscos identificados", value=defaults.get("riscos", ""), height=80)
    alinhamento = st.text_area("Alinhamento estratégico", value=defaults.get("alinhamento", ""), height=80)

    submitted = st.form_submit_button("💾 Gerar rascunho do DFD")

# ==========================================================
# 💾 Resultado e Feedback
# ==========================================================
if submitted:
    st.success("✅ Rascunho de DFD gerado com sucesso!")
    dfd_data = {
        "unidade": unidade,
        "responsavel": responsavel,
        "objeto": objeto,
        "justificativa": justificativa,
        "quantidade": quantidade,
        "urgencia": urgencia,
        "riscos": riscos,
        "alinhamento": alinhamento,
    }

    st.json(dfd_data)
    st.info("Os dados foram processados e podem ser exportados ou validados em etapas posteriores.")
    st.session_state["last_dfd"] = dfd_data  # 🔄 guarda para uso futuro (TR, Edital, etc.)

# ==========================================================
# 📊 Observações Técnicas
# ==========================================================
st.divider()
st.caption(
    """
    💡 *Dica:* Quando um insumo for processado na aba **Insumos**, o DFD será automaticamente pré-preenchido.  
    O campo `st.session_state["last_insumo"]` é utilizado para transferir as inferências da IA entre páginas.*
    """
)
