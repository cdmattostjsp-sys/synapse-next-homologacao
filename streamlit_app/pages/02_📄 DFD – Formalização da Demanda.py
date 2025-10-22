import streamlit as st

st.set_page_config(page_title="📄 DFD – Formalização da Demanda", layout="wide")

st.title("📄 DFD – Documento de Formalização da Demanda")
st.caption("Pré-preenchimento automático a partir de insumos + validação IA")

# Detecta insumo ativo (mas sem obrigar o envio)
insumo = st.session_state.get("last_insumo")

if insumo and insumo.get("artefato") == "DFD":
    st.success(f"📎 Insumo ativo detectado: {insumo['nome']} (Artefato: {insumo['artefato']})")
    with st.expander("Prévia do insumo (texto legível)", expanded=False):
        st.text(insumo.get("conteudo", "")[:1500])
    defaults = insumo.get("campos_ai", {}) or {}
else:
    st.info("Nenhum insumo ativo encontrado. Você pode preencher manualmente ou enviar um documento na aba **🔧 Insumos**.")
    defaults = {}

# Formulário institucional (com ou sem preenchimento automático)
st.subheader("1️⃣ Entrada – Formulário institucional")

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
